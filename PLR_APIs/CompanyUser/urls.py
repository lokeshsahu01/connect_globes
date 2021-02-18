from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', company_login_view, name='company_login_view'),
    path('logout/', user_logout_view, name='user_logout_view'),

    path('sub-user/create/', company_sub_user_create_view, name='company_sub_user_create_view'),
    path('sub-user/update/<str:pk>/', company_sub_user_create_view, name='company_sub_user_update_view'),
    path('sub-user/get/', company_sub_user_create_view, name='company_sub_user_get_view'),
    path('sub-user/get/<str:pk>/', company_sub_user_create_view, name='company_sub_user_get_one_view'),

    path('user-level/get/', create_user_level_view, name='user-level-view-get'),
    path('user-level/add/', create_user_level_view, name='user-level-view-add'),
    path('user-level/update/<str:pk>/', create_user_level_view, name='user-level-view-update'),
    path('user-level/delete/<str:pk>/', create_user_level_view, name='user-level-view-delete'),
    path('user-level/get/<str:pk>/', create_user_level_view, name='user-level-view-get-one'),

    path('user-department/get/', user_department_view, name='user-department-view-get'),
    path('user-department/add/', user_department_view, name='user-department-view-add'),
    path('user-department/update/<str:pk>/', user_department_view, name='user-department-view-update'),
    path('user-department/delete/<str:pk>/', user_department_view, name='user-department-view-delete'),
    path('user-department/get/<str:pk>/', user_department_view, name='user-department-view-get-one'),

    path('sub-user/activate/update/<str:pk>/', user_activate_view, name='user-activate-view-update'),
    path('sub-user/count/get/', get_total_user, name='company_sub_user_get_view'),

]