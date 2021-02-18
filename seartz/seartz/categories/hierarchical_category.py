from .models import *
from django.forms.models import model_to_dict
import os, sys
from django.http import JsonResponse


def parent_tree_category(parent_user):

    def child_tree_category(parent_user, sub_c_user):
        if parent_user.sub_category is None:
            return sub_c_user + f"/{parent_user.slug}"
        else:
            child_user = Categories.objects.get(id=parent_user.id)
            sub_c_user += f"/{child_user.slug}"
            sub_c_user = child_tree_category(Categories.objects.get(id=child_user.sub_category), sub_c_user)
            return sub_c_user
    return child_tree_category(parent_user, "")


def child_tree_category(parent_user):

    def child_category(parent_user, sub_c_user, c):
        if Categories.objects.filter(sub_category=parent_user).exists():
            for i in Categories.objects.filter(sub_category=parent_user):
                k = model_to_dict(i)
                if 'category_image' in k and k['category_image'] is not None and i.category_image.name != '':
                    k['category_image'] = i.category_image.url
                else:
                    k['category_image'] = None
                sub_c_user.append(k)
                c += 1
                sub_c_user = child_category(i.id, sub_c_user, c)
            return sub_c_user
        else:
            c -= 1
            return sub_c_user
    return child_category(parent_user, [], 1)


def child_name_tree_category(parent_user):

    def child_name_category(parent_user, sub_c_user, c):
        if Categories.objects.filter(sub_category=parent_user).exists():
            for i in Categories.objects.filter(sub_category=parent_user):
                sub_c_user.append(i.category_name)
                c += 1
                sub_c_user = child_name_category(i.id, sub_c_user, c)
            return sub_c_user
        else:
            c -= 1
            return sub_c_user
    return child_name_category(parent_user, [], 1)


def space_tree_category(parent_user):
    def tree_category(parent_user, sub_c_user):
        if parent_user.sub_category is None:
            return sub_c_user
        else:
            child_user = Categories.objects.get(id=parent_user.id)
            sub_c_user += "--"
            sub_c_user = tree_category(child_user.sub_category, sub_c_user)
            return sub_c_user
    return tree_category(parent_user, "")


def category_json(obj):
    try:
        k = model_to_dict(obj)
        if 'category_image' in k and k['category_image'] is not None and obj.category_image.name != '':
            k['category_image'] = obj.category_image.url
        else:
            k['category_image'] = None
        return k
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return {'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}


def get_categories(default):
    if default:
        cat_list = [('', '---------')]
    else:
        cat_list = []
    for obj in Categories.objects.filter(sub_category=None):
        d = child_name_tree_category(obj.id)
        d[:0] = [obj.category_name, ]
        for i in d:
            cat_list.append((i.strip('-'), i.strip(' ')))
    return cat_list


def category_all(obj):
    Categories.objects.aggregate()