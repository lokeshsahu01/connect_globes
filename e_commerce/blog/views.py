from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from .models import *


@api_view(['GET', ])
def update_popular_blog_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = Blog.objects.get(id=pk)
            if prod.is_popular:
                prod.is_popular = False
            else:
                prod.is_popular = True
            prod.save()
        return redirect('/admin/blog/blog/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_active_blog_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = Blog.objects.get(id=pk)
            if prod.is_active:
                prod.is_active = False
            else:
                prod.is_active = True
            prod.save()
        return redirect('/admin/blog/blog/')
    return redirect('/admin/login/')
