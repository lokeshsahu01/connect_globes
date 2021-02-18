from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('get/all/', get_category_view, name="get_category"),
    path('show/', show_categories, name="get_category"),
    path('show/<int:pk>/', show_categories, name="get_one_category"),
]
