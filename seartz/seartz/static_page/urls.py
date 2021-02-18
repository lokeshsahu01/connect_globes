from django.urls import path
from .views import *

urlpatterns = [
    path('our-team/get/', our_team_view, name="our_team"),
    path('vision/get/', vision_view, name="vision"),
    path('mission/get/', mission_view, name="mission"),
    path('fandq/get/', f_and_q_view, name="f_and_q"),
]
