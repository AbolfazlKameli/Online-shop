from django.contrib import admin
from .models import Order, OrderItem, Coupon, PayInfo


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'paid')
    list_filter = ('paid', 'created', 'updated')
    inlines = (OrderItemInline,)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'expires_at', 'discount', 'active')


@admin.register(PayInfo)
class PayInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'reference_id', 'created')
    list_filter = ('user', 'created')
    search_fields = ('user__phone_number', 'reference_id')
