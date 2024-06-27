from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View

from bucket import bucket
from utils import IsSellerUserMixin
from .forms import AddEditProductForm
from home.models import Product


class AddProductView(IsSellerUserMixin, View):
    template_name = 'seller/add_product.html'
    from_class = AddEditProductForm

    def get(self, request):
        form = AddEditProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddEditProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_product = form.save(commit=False)
            new_product.slug = slugify(cd['name'][:50])
            bucket.upload_object(request, form.cleaned_data['filename'])
            new_product.save()
            messages.success(request, 'added product', extra_tags='success')
            return redirect('users:user_profile')
        messages.error(request, 'an error occurred', extra_tags='danger')
        return render(request, self.template_name, {'form': form})


class EditProductView(IsSellerUserMixin, View):
    template_name = 'seller/edit_product.html'
    from_class = AddEditProductForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, id=kwargs['product_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.from_class(instance=self.product_instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST, request.FILES, instance=self.product_instance)
        if form.is_valid():
            cd = form.cleaned_data
            updated_product = form.save(commit=False)
            updated_product.slug = slugify(cd['name'][:50])
            updated_product.image = cd['filename']
            bucket.upload_object(request, form.cleaned_data['filename'])
            updated_product.save()
            messages.success(request, 'edited product', extra_tags='success')
            return redirect('users:user_profile')
        messages.error(request, 'an error occurred', extra_tags='danger')
        return render(request, self.template_name, {'form': form})
