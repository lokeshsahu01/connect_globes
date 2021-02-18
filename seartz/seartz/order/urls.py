from django.urls import path
from .views import *

urlpatterns = [
    path('cart/create/', create_cart_view, name="create_cart"),
    path('cart/edit/<int:pk>/', edit_cart_view, name="edit_cart"),
    path('cart/delete/<int:pk>/', delete_cart_view, name="delete_cart"),
    path('cart/get/<int:pk>/', get_cart_view, name="get_one_cart"),
    path('cart/get/', get_cart_view, name="get_all_cart"),
    path('address/get/', get_order_address_view, name="get_order_address"),
    path('address/get/<int:pk>/', get_order_address_view, name="get_one_order_address"),
    path('address/create/', create_order_address_view, name="create_order_address"),
    path('address/edit/<int:pk>/', edit_order_address_view, name="edit_order_address"),
    path('create/', create_order_view, name='create_order'),
    path('get/', get_order_view, name='get_order'),
    path('get/<str:order_id>/', get_order_view, name='get_order'),
    path('edit/<str:order_id>/<int:product_id>/', cancel_order_view, name='edit_order_view'),
    path('payment/', create_rozor_payment_view),
    path('payment/success', success, name='success')
]
