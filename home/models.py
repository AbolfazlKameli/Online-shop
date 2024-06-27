from django.db import models
from django.urls import reverse

from users.models import User


# Create your models here.
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='s_category')
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug, ])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Ucomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='Rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=450)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.is_reply}'
