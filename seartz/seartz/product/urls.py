from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_product_view, name="create_product"),
    path('edit/<int:pk>/', edit_product_view, name="edit_product"),
    path('get/', get_product_view, name="get_product"),
    path('get/user/<int:pk>/', get_users_product_view, name="get_users_product"),
    path('get/user/', get_users_product_view, name="get_users_product"),
    path('get/<int:pk>/', get_one_product_view, name="get_one_product"),
    path('get/slug/<str:slug>/', get_one_slug_product_view, name="get_one_slug_product"),
    path('feature/<int:pk>/', update_feature_product_view, name="update_feature_product"),
    path('get/category/<str:category>/', get_product_category_view, name="get_product_category"),
    path('heart/create/<int:prodid>/', create_product_heart_view, name="create_product_heart"),
    path('view/create/<int:prodid>/', create_product_view_view, name="create_product_view"),
    path('comment/create/<int:prodid>/', create_product_total_comment_view, name="create_product_total_comment"),
    path('review/create/<int:prodid>/', create_product_total_review_view, name="create_product_total_review"),
    path('size/create/<int:prodid>/', create_product_size_view, name="create_product_size"),
]
