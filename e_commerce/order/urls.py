from django.urls import path
from .views import *

urlpatterns = [
    path('coupon/feature/<int:pk>/', update_feature_coupon_view, name="update_feature_coupon"),
    path('coupon/valid/<int:pk>/', update_valid_coupon_view, name="update_valid_product"),
]
