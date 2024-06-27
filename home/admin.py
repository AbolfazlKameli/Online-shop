from django.contrib import admin

from .models import Category, Product, Comment


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'id')
    list_filter = ('category', 'available')
    raw_id_fields = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub', 'sub_category')
    list_filter = ('is_sub',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'is_reply', 'created', 'id')
