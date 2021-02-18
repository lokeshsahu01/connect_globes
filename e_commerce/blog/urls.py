from django.urls import path
from .views import *

urlpatterns = [
    path('popular/<int:pk>/', update_popular_blog_view, name="update_popular_blog"),
    path('active/<int:pk>/', update_active_blog_view, name="update_active_blog"),
]
