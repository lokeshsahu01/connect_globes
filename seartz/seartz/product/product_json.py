from django.forms.models import model_to_dict
import os, sys
from .models import *


def json_product(obj):
    try:
        product_list = []
        for i in obj:
            k = model_to_dict(i)
            k['product_home_image'] = i.product_home_image.url if i.product_home_image.name else i.product_home_image.name
            k['product_gallery_image'] = []
            if ProductGalleryImage.objects.filter(product_id=i).exists():
                for j in ProductGalleryImage.objects.filter(product_id=i):
                    k['product_gallery_image'].append(j.product_gallery_image.url if j.product_gallery_image.name else j.product_gallery_image.name)
            k['certificate_file'] = i.certificate_file.name
            product_list.append(k)
        return product_list
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return {'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}


def one_product_json(obj):
    k = model_to_dict(obj)
    k['product_home_image'] = obj.product_home_image.url if obj.product_home_image.name else obj.product_home_image.name
    k['product_gallery_image'] = []
    k['price_off'] = k['price_off'] if k['price_off'] else 0
    if ProductGalleryImage.objects.filter(product_id=obj).exists():
        for i in ProductGalleryImage.objects.filter(product_id=obj):
            k['product_gallery_image'].append(i.product_gallery_image.url if i.product_gallery_image.name else i.product_gallery_image.name)
    k['certificate_file'] = obj.certificate_file.name
    return k
