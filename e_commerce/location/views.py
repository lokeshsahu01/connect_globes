from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from .models import *


@api_view(['GET', ])
def update_popular_state_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            count = State.objects.get(id=pk)
            if count.is_popular:
                count.is_popular = False
            else:
                count.is_popular = True
            count.save()
        return redirect('/admin/location/state/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_active_state_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            count = State.objects.get(id=pk)
            if count.is_active:
                count.is_active = False
            else:
                count.is_active = True
            count.save()
        return redirect('/admin/location/state/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_active_city_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            count = City.objects.get(id=pk)
            if count.is_active:
                count.is_active = False
            else:
                count.is_active = True
            count.save()
        return redirect('/admin/location/city/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_popular_city_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            count = City.objects.get(id=pk)
            if count.is_popular:
                count.is_popular = False
            else:
                count.is_popular = True
            count.save()
        return redirect('/admin/location/city/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_active_pincode_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            count = Pincode.objects.get(id=pk)
            if count.is_active:
                count.is_active = False
            else:
                count.is_active = True
            count.save()
        return redirect('/admin/location/pincode/')
    return redirect('/admin/login/')



