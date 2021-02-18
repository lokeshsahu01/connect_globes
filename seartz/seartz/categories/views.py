from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from rest_framework.response import Response
from django.http import JsonResponse
from .models import *
from .hierarchical_category import *
import os, sys
from seartz.mongoDBConnection import *


@api_view(['GET', ])
def category_url_view(request, slug=None):
    try:
        url = [i for i in slug.split('/') if i != '']
        for i in url:
            if not Categories.objects.filter(slug=i).exists():
                return JsonResponse({'error': 'Url Not Found'}, safe=False, status=404)
        slug_obj = category_json(Categories.objects.get(slug=url[-1]))
        return JsonResponse(slug_obj, safe=False,  status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, safe=False, status=500)


@api_view(['GET', ])
def get_category_view(request, slug=None):
    cats = []
    for i in Categories.objects.filter(sub_category=None):
        sub_cats = child_tree_category(i.id)
        k = model_to_dict(i)
        if 'category_image' in k and k['category_image'] is not None and i.category_image.name != '':
            k['category_image'] = i.category_image.url
        else:
            k['category_image'] = None
        k['SubCategory'] = sub_cats
        cats.append(k)
    return JsonResponse({"data": cats, "message": "Successfully Get Categories", "status": 200}, status=200)


@api_view(['GET', ])
def get_category_all_view(request, slug=None):
    category_model = database['categories_categories']
    cats = []

    group = [{
            '$match': {
                    'sub_category': None
                }
            }, {
                  '$graphLookup': {
                    'from': "categories_categories",
                    'startWith': "$id",
                    'connectFromField': "id",
                    'connectToField': "sub_category",
                    'depthField': "level",
                    'as': "SubCategories"
                  }
                }, {
                  '$unwind': {
                    'path': "$SubCategories",
                    'preserveNullAndEmptyArrays': True
                  }
                }, {
                  '$sort': {
                    "SubCategories.level": -1
                  }
                }, {
                  '$group': {
                    '_id': "$id",
                    'id': {'$first': "$id"},
                    'sub_category': {'$first': "$sub_category"},
                    'category_name': {'$first': "$category_name"},
                    'category_description': {'$first': "$category_description"},
                    'status': {'$first': "$status"},
                    'category_image': {'$first': "$category_image"},
                    'slug': {'$first': "$slug"},
                    'meta_description': {'$first': "$meta_description"},
                    'meta_keyword': {'$first': "$meta_keyword"},
                    'created_at': {'$first': "$created_at"},
                    'SubCategories': {'$push': "$SubCategories"}
                  }
                }, {
                  '$addFields': {
                    'SubCategories': {
                      '$reduce': {
                        'input': "$SubCategories",
                        'initialValue': {
                          'level': -1,
                          'presentChild': [],
                          'prevChild': []
                        },
                        'in': {
                          '$let': {
                            'vars': {
                              'prev': {
                                '$cond': [
                                  {
                                    '$eq': [
                                      "$$value.level",
                                      "$$this.level"
                                    ]
                                  },
                                  "$$value.prevChild",
                                  "$$value.presentChild"
                                ]
                              },
                              'current': {
                                '$cond': [
                                  {
                                    '$eq': [
                                      "$$value.level",
                                      "$$this.level"
                                    ]
                                  },
                                  "$$value.presentChild",
                                  []
                                ]
                              }
                            },
                            'in': {
                              'level': "$$this.level",
                              'prevChild': "$$prev",
                              'presentChild': {
                                '$concatArrays': [
                                  "$$current",
                                  [
                                    {
                                      'id': "$$this.id",
                                      'category_name': "$$this.category_name",
                                      'sub_category': "$$this.sub_category",
                                      'slug': "$$this.slug",
                                      'category_description': "$$this.category_description",
                                      'status': "$$this.status",
                                      'category_image': "$$this.category_image",
                                      'meta_description': "$$this.meta_description",
                                      'meta_keyword': "$$this.meta_keyword",
                                      'created_at': "$$this.created_at",
                                      'SubCategories': {
                                        '$filter': {
                                          'input': "$$prev",
                                          'as': "e",
                                          'cond': {
                                            '$eq': [
                                              "$$e.sub_category",
                                              "$$this.id"
                                            ]
                                          }
                                        }
                                      }
                                    }
                                  ]
                                ]
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }, {
                  '$addFields': {
                    'SubCategories': "$SubCategories.presentChild"
                  }
                }
    ]

    d = category_model.aggregate(group)
    for i in d:
        i.pop('_id')
        cats.append(i)
    return JsonResponse({"data": cats, "message": "Successfully Get All Categories", "status": 200}, status=200)
