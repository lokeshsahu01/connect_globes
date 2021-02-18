from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from .models import *


@api_view(['GET', ])
def update_feature_product_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = Product.objects.get(id=pk)
            if prod.is_feature:
                prod.is_feature = False
            else:
                prod.is_feature = True
            prod.save()
        return redirect('/admin/products/product/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_gallery_image_feature_product_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = ProductGalleryImage.objects.get(id=pk)
            ProductGalleryImage.objects.filter(product=prod.product).update(is_feature=False)
            if prod.is_feature:
                prod.is_feature = False
            else:
                prod.is_feature = True
            prod.save()
            return redirect(f'/admin/products/productgalleryimage/?product__id={prod.product.id}')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_gallery_video_feature_product_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = ProductGalleryVideo.objects.get(id=pk)
            ProductGalleryVideo.objects.filter(product=prod.product).update(is_feature=False)
            if prod.is_feature:
                prod.is_feature = False
            else:
                prod.is_feature = True
            prod.save()
            return redirect(f'/admin/products/productgalleryvideo/?product__id={prod.product.id}')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_status_product_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = Product.objects.get(id=pk)
            if prod.status:
                prod.status = False
            else:
                prod.status = True
            prod.save()
        return redirect('/admin/products/product/')
    return redirect('/admin/login/')


@api_view(['GET', ])
def update_approved_product_view(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            prod = Product.objects.get(id=pk)
            if prod.is_approved:
                prod.is_approved = False
                prod.approved_by = None
            else:
                prod.is_approved = True
                prod.approved_by = User.objects.get(id=request.user.id)
            prod.save()
        return redirect('/admin/products/product/')
    return redirect('/admin/login/')
