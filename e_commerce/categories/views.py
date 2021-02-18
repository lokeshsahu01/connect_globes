from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import *
from django.http import JsonResponse


@api_view(['GET', ])
def get_category_view(request, slug=None):
    cats = CategoriesSerializer(Categories.objects.filter(parent=None), many=True)
    return JsonResponse({"data": cats.data, "message": "Successfully Get Categories", "status": 200}, status=200)


def show_categories(request, pk=None):
    if pk:
        cat = Categories.objects.filter(id=pk) | Categories.objects.get(id=pk).get_descendants(include_self=True)
        return render(request, "project/categories.html", {'categories': cat})
    return render(request, "project/categories.html", {'categories': Categories.objects.all()})
