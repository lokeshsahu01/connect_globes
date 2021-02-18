from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login_view, name="user_login"),
    path('home/', home_view, name="home_view")
]
