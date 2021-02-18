from django.forms.models import model_to_dict
import os, sys
from .models import *


def json_product(obj):
    home_slider_list = []
    for i in obj:
        k = model_to_dict(i)
        k['slider_image'] = i.slider_image.url if i.slider_image.name else i.slider_image.name
        home_slider_list.append(k)
    return home_slider_list
