from django.urls import path
from .views import *

urlpatterns = [
    path('group/get/', group_view, name='get_group_view'),
    path('group/create/', group_view, name='create_group_view'),
    path('group/update/<str:pk>/', group_view, name='update_group_view'),
    path('group/delete/<str:pk>/', group_view, name='delete_group_view'),
    path('group/get/<str:pk>/', group_view, name='get_one_group_view'),

    path('create/', task_view, name='create_task_view'),
    path('get/', get_task_view, name='get_task_view'),
    path('get/<str:pk>/', get_task_view, name='get_one_task_view'),
    path('update/<str:pk>/', task_view, name='update_task_view'),
    path('delete/<str:pk>/', task_view, name='delete_task_view'),

    path('comment/create/', task_comment_view, name="create_task_comment_view"),
    path('comment/get/', task_comment_view, name="get_task_comment_view"),
    path('comment/update/<str:pk>/', task_comment_view, name="update_task_comment_view"),
    path('comment/delete/<str:pk>/', task_comment_view, name="delete_task_comment_view"),

    path('file-management/create/', task_file_management_view, name="create_task_file_management_view"),
    path('file-management/get/', task_file_management_view, name="get_task_file_management_view"),
    path('file-management/delete/<str:pk>/', task_file_management_view, name="delete_task_file_management_view"),
    path('file-management/get/<str:pk>/', task_file_management_view, name="get_one_task_file_management_view"),

    path('reassign/<str:pk>/', reassign_task_view, name='reassign_task_view'),
    path('log-activity/get/', task_log_activity_view, name='task_log_activity_view'),
]
