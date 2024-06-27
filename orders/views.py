import json
from datetime import datetime, timedelta

import pytz
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from home.models import Product
from utils import IsAdminUserMixin
from .cart import Cart
from .forms import CartAddForm, CouponApplyForm
from .models import Order, OrderItem, Coupon, PayInfo


# Create your views here.
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
            messages.success(request, f'{product.name} added to your cart', extra_tags='success')
        return redirect('home:product_detail', product.slug)


class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        cart = Cart(request)
        if str(product_id) in request.session['cart'].keys():
            product = get_object_or_404(Product, id=product_id)
            cart.remove(product)
            messages.success(request, f'removed {product.name} from your cart')
            return redirect('orders:cart')
        messages.error(request, 'this item is not in your cart', extra_tags='danger')
        return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=int(item['price']),
                                     quantity=item['quantity'])
        cart.clear()
        messages.info(request, 'your order created')
        return redirect('orders:order_detail', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order_detail.html', {'order': order, 'form': self.form_class})


class OrderDeleteView(IsAdminUserMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order:
            order.delete()
            messages.success(request, 'order deleted successfully', extra_tags='success')
        return redirect('home:home')


class ZPPayView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.order_instance = get_object_or_404(Order, id=kwargs['order_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        expired = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(days=1)
        if self.order_instance.created < expired or self.order_instance.paid:
            messages.info(request, 'this order expired or paid in the past', extra_tags='info')
            return redirect('users:user_profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id):
        order = self.order_instance
        print(order)
        request.session['order_pay'] = {
            'order_id': order_id
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": settings.DESCRIPTION,
            "Phone": request.user.phone_number,
            "CallbackURL": settings.CALLBACKURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response_json = response.json()
                authority = response_json['Authority']
                if response_json['Status'] == 100:
                    return redirect(settings.ZP_API_STARTPAY + authority)
                else:
                    return HttpResponse('Error')
            return HttpResponse('response failed')
        except requests.exceptions.Timeout:
            return HttpResponse('Timeout Error')
        except requests.exceptions.ConnectionError:
            return HttpResponse('Connection Error')


class ZPPayVerifyView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        if status == 'OK' and authority:
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": order.get_total_price(),
                "Authority": authority,
            }
            data = json.dumps(data)
            # set content length by data
            headers = {'accept': 'application/json', 'content-type': 'application/json',
                       'content-length': str(len(data))}
            try:
                response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)
                if response.status_code == 200:
                    response_json = response.json()
                    reference_id = response_json['RefID']
                    if response_json['Status'] == 100:
                        order.paid = True
                        PayInfo.objects.create(user=request.user, order=order, reference_id=reference_id).save()
                        order.save()
                        messages.success(request, f'successful, RefID: {reference_id}', extra_tags='success')
                        return render(request, self.template_name, {'reference': reference_id})
                    else:
                        return render(request, self.template_name, {'error': 'Error'})
                return render(request, self.template_name, {'error': 'response failed'})
            except requests.exceptions.Timeout:
                return render(request, self.template_name, {'error': 'TimeOutError'})
            except requests.exceptions.ConnectionError:
                return render(request, self.template_name, {'error': 'ConnectionError'})
        else:
            return render(request, self.template_name, {'error': 'Not OK'})


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lt=now, expires_at__gt=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon is invalid pr expired', extra_tags='danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            messages.success(request, f'{coupon.code} applied', extra_tags='success')
            return redirect('orders:order_detail', order_id)
