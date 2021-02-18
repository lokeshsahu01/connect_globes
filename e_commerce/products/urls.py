from django.urls import path
from .views import *

urlpatterns = [
    path('feature/<int:pk>/', update_feature_product_view, name="update_feature_product"),
    path('gallery/image/feature/<int:pk>/', update_gallery_image_feature_product_view, name="update_gallery_image_feature_product"),
    path('gallery/video/feature/<int:pk>/', update_gallery_video_feature_product_view, name="update_gallery_video_feature_product"),
    path('status/<int:pk>/', update_status_product_view, name="update_status_product"),
    path('approve/<int:pk>/', update_approved_product_view, name="update_approved_product"),
]
