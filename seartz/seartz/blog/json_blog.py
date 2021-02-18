from django.forms.models import model_to_dict
from .models import *


def blog_to_json(obj):

    k = model_to_dict(obj)
    k['blog_images'] = []
    if BlogImage.objects.filter(user_id=obj.user_id, blog_id=obj.id).exists():
        for i in BlogImage.objects.filter(user_id=obj.user_id, blog_id=obj.id):
            j = model_to_dict(i)
            j['blog_image'] = j['blog_image'].url
            k['blog_images'].append(j)
    return k


def all_blog_to_json(obj):
    all = []
    for i in obj:
        k = model_to_dict(i)
        k['blog_images'] = []
        if BlogImage.objects.filter(user_id=i.user_id, blog_id=i.id).exists():
            for g in BlogImage.objects.filter(user_id=i.user_id, blog_id=i.id):
                j = model_to_dict(g)
                j['blog_image'] = j['blog_image'].url
                k['blog_images'].append(j)
        all.append(k)
    return all


def one_blog_to_json(obj):
    k = model_to_dict(obj)
    k['blog_images'] = []
    if BlogImage.objects.filter(user_id=obj.user_id, blog_id=obj.id).exists():
        for i in BlogImage.objects.filter(user_id=obj.user_id, blog_id=obj.id):
            j = model_to_dict(i)
            j['blog_image'] = j['blog_image'].url
            k['blog_images'].append(j)
    return k


def blog_comment_json(obj):
    comment_list = []
    for i in obj:
        k = model_to_dict(i)
        comment_list.append(k)
    return comment_list
