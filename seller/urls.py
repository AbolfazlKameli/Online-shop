from django.urls import path
from . import views

app_name = 'seller'
urlpatterns = [
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('edit_product/<int:product_id>/', views.EditProductView.as_view(), name='edit_product'),
]
