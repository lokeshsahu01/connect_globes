from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'^urls/(?P<slug>.+)$', category_url_view, name="user_login"),
    path('namelist/get/', get_category_view, name="get_namelist_category_view"),
    path('get/all/', get_category_all_view, name="get_all_category_view"),
]
