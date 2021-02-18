from django.urls import path
from .views import *

urlpatterns = [
    path('slider/get/', home_slider_view, name="home_slider"),
    path('slider/feature/<int:pk>/', update_feature_home_slider_view, name="update_feature_home_slider"),
    path('admin/dashboard/', dashboard_view),
    path('gallery/category/get/', gallery_category_view, name="home_gallery_category_get"),
    path('gallery/category/get/<int:pk>', gallery_category_view, name="home_gallery_category_get_one"),
    path('contact-us/get/', contact_us_view, name="contact_us"),
    path('about-us/get/', about_us_view, name="about_us"),
    path('contact-us/create/', create_contact_us_view, name="create_contact_us"),
    path('testimonial/get/', testimonial_view, name="testimonial"),
    path('testimonial/feature/<int:pk>/', update_feature_testimonial_view, name="testimonial_feature"),
]
