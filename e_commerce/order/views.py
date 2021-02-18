from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from .models import *


@api_view(['GET', ])
def update_feature_coupon_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            coup = CouponCode.objects.get(id=pk)
            if coup.is_feature:
                coup.is_feature = False
            else:
                coup.is_feature = True
            coup.save()
        return redirect('/admin/order/couponcode/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_valid_coupon_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            coup = CouponCode.objects.get(id=pk)
            if coup.is_valid:
                coup.is_valid = False
            else:
                coup.is_valid = True
            coup.save()
        return redirect('/admin/order/couponcode/')
    return redirect('/admin/login/')
