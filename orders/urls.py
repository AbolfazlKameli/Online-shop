from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('delete/<int:order_id>/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('cart/add/<int:product_id>', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>', views.CartRemoveView.as_view(), name='cart_remove'),
    path('pay/<int:order_id>/', views.ZPPayView.as_view(), name='pay'),
    path('verify/', views.ZPPayVerifyView.as_view(), name='verify'),
    path('coupon/apply/<int:order_id>/', views.CouponApplyView.as_view(), name='coupon_apply'),
]
