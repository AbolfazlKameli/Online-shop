from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from bucket import bucket
from orders.forms import CartAddForm
from utils import IsAdminUserMixin
from . import tasks
from .forms import UploadFileForm, CommentCreateForm, CommentReplyForm
from .models import Product, Category, Comment


# Create your views here.
class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.all()
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, 'home/home.html', context)


class ProductDetailView(View):
    form_class = CommentCreateForm
    form_reply_class = CommentReplyForm
    template_name = 'home/detail.html'

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product_instance
        comments = self.product_instance.Pcomments.filter(is_reply=False)
        form = CartAddForm()
        return render(request, self.template_name,
                      {'product': product, 'form': form, 'comments': comments, 'comment_create_form': self.form_class,
                       'reply_form': self.form_reply_class})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product_instance
            new_comment.save()
            messages.success(request, 'Your comment submitted', extra_tags='success')
            return redirect('home:product_detail', self.product_instance.slug)


class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'
    form_class = UploadFileForm

    def get(self, request):
        objects = tasks.get_bucket_objects_task()
        form = self.form_class()
        return render(request, self.template_name, {'objects': objects, 'form': form})


class BucketHomeObjectDelete(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'the object will delete soon', extra_tags='info')
        return redirect('home:bucket_home')


class BucketHomeObjectDownload(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.info(request, 'the object will download soon', extra_tags='info')
        return redirect('home:bucket_home')


class BucketHomeObjectUpload(IsAdminUserMixin, View):
    form_class = UploadFileForm

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            bucket.upload_object(request, form.cleaned_data['filename'])
        return redirect('home:bucket_home')


class CreatCommentReplyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            form.save()
            messages.success(request, 'your comment submitted', extra_tags='success')
        return redirect('home:product_detail', product.slug)


class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user.id == comment.user.id:
            comment.delete()
            messages.success(request, 'deleted', extra_tags='success')
        else:
            messages.error(request, 'cant delete other users comments', extra_tags='warning')
        return redirect('home:product_detail', comment.product.slug)
