from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_blog_view, name="create_blog"),
    path('edit/<int:pk>/', create_blog_view, name="edit_blog"),
    path('get/<int:pk>/', get_blog_view, name="get_one_blog"),
    path('delete/<int:pk>/', delete_blog_view, name="delete_one_blog"),
    path('get/', get_blog_view, name="get_blog"),
    path('user/get/', users_blog_view, name="user_get_blog"),
    path('approved/<int:blog_id>/', create_blog_comment_view, name="approved_blog_heart"),
    path('heart/create/<int:blog_id>/', create_blog_heart_view, name="create_blog_heart"),
    path('view/create/<int:blog_id>/', create_blog_view_view, name="create_view_heart"),
    path('comment/create/<int:blog_id>/', create_blog_comment_view, name="create_comment_heart"),
    path('comment/approved/<int:comment_id>/', approval_blog_comment_view, name="approved_comment_heart"),
    path('approved/<int:blog_id>', approval_blog_view, name="approved_blog"),
]
