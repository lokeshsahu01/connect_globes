from django.urls import path
from .views import *

urlpatterns = [
    path('folder/get/', folder_view, name='get_folder_view'),
    path('folder/create/', folder_view, name='create_folder_view'),
    path('folder/update/<str:pk>/', folder_view, name='update_folder_view'),
    path('folder/delete/<str:pk>/', folder_view, name='delete_folder_view'),
    path('folder/get/<str:pk>/', folder_view, name='get_one_folder_view'),

    path('upload-file/create/', create_dms_view, name='create_dms_view'),
    path('upload-file/get/', dms_view, name='get_dms_view'),
    path('upload-file/get/<str:pk>/', dms_view, name='get_one_dms_view'),
    path('upload-file/update/<str:pk>/', dms_view, name='update_dms_view'),
    path('upload-file/delete/<str:pk>/', dms_view, name='delete_dms_view'),
]
