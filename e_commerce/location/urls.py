from django.urls import path
from .views import *

urlpatterns = [
    path('state/popular/<int:pk>/', update_popular_state_view, name="update_popular_state"),
    path('state/active/<int:pk>/', update_active_state_view, name="update_active_state"),
    path('city/popular/<int:pk>/', update_popular_city_view, name="update_active_city"),
    path('city/active/<int:pk>/', update_active_city_view, name="update_popular_city"),
    path('pincode/active/<int:pk>/', update_active_pincode_view, name="update_active_pincode"),
]
