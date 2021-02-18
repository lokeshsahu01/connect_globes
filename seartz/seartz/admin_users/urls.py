from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login_view, name="user_login"),
    path('artist/login/', artist_user_login_view, name="artist_user_login"),
    path('password/change/', user_password_change, name="home_view"),
    path('login/otp/send/', login_opt_send_view, name="login_opt_send"),
    path('login/otp/verify/', login_opt_verify_view, name="login_opt_verify"),
    path('artist/login/otp/verify/', artist_login_opt_verify_view, name="artist_login_opt_verify"),
    path('artist/get/', get_artist_junior_view, name="get_artist_junior"),
    path('artist/profile/edit/', create_artist_junior_view, name="create_artist_junior_profile"),
]
