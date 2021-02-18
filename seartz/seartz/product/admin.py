from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages
import os, sys
from categories.models import *
from django.contrib.admin.filters import RelatedOnlyFieldListFilter, RelatedFieldListFilter
from django.utils.html import format_html
from categories.models import *


class ProductAdminView(admin.ModelAdmin):
    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    def category_name(self, obj):
        category = Categories.objects.get(id=obj.category_id)
        html = f'''<a href="/admin/categories/categories/{category.id}/change/">{category.category_name}</a>'''
        return format_html(html)

    def url(self, obj):
        html = f'''<a href="http://paperlessrack.in/detailpage/{obj.slug}">{obj.slug}</a>'''
        return format_html(html)

    def feature(self, obj):
        if obj.is_feature:
            html = f'''<a href="/api/v1/products/feature/{obj.id}"><img src="/static/admin/img/icon-no.svg" alt="False"></a>'''
        else:
            html = f'''<a href="/api/v1/products/feature/{obj.id}"><img src="/static/admin/img/icon-yes.svg" alt="True"></a>'''
        return format_html(html)

    def product_price(self, obj):
        if obj.selling_price == 0 or obj.selling_price is None or obj.selling_price == '':
            return obj.price
        else:
            return obj.selling_price

    list_display = ['id', 'product_code', 'product_name', 'username', 'category_name', 'product_price', 'url', 'status',
                    'feature', 'created_at']
    # list_filter = ('category__category_name', 'status')
    list_editable = ('status', )
    search_fields = ('product_name', 'slug', 'user__username', 'product_code', 'category__category_name',)
    form = ProductForm

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields['product_category'].initial = Categories.objects.get(id=obj.category_id).category_name
            if ProductGalleryImage.objects.filter(product_id=obj.id).exists():
                filename = " "
                for i in ProductGalleryImage.objects.filter(product_id=obj.id):
                    filename += f'''<a href="/admin/product/productgalleryimage/{i.id}/change/"><img src="{i.product_gallery_image.url}" alt="Product Gallery Image" width="50" height="50" style="padding:5px"></a>'''
                form.base_fields['product_gallery_image'].help_text = filename

            if obj.product_home_image.name != '' and obj.product_home_image.name is not None:
                form.base_fields['product_home_image'].help_text = f'<img src="{obj.product_home_image.url}" alt="Product Home Image" width="80" height="80">'
        else:
            form.base_fields['product_home_image'].help_text = ""
        return form

    def save_model(self, request, obj, form, change):
        try:
            form.cleaned_data['user_id'] = request.user.id
            product_gallery_files = None
            if 'product_gallery_image' in request.FILES and request.FILES['product_gallery_image'] is not None:
                product_gallery_files = request.FILES.getlist('product_gallery_image')
            if 'product_gallery_image' in form.cleaned_data:
                del form.cleaned_data['product_gallery_image']
            if obj.id is None:
                Product(**form.cleaned_data).save()
                prod_obj = Product.objects.last()
            else:
                if 'product_home_image' in form.cleaned_data and form.cleaned_data['product_home_image'] and form.cleaned_data['product_home_image'] != '':
                    prod_obj = Product.objects.get(id=obj.id)
                    prod_obj.product_home_image = form.cleaned_data['product_home_image']
                    prod_obj.save()
                    del form.cleaned_data['product_home_image']
                if 'id' in form.cleaned_data:
                    del form.cleaned_data['id']
                if 'user_id' in form.cleaned_data:
                    del form.cleaned_data['user_id']
                Product.objects.filter(id=obj.id).update(**form.cleaned_data)
                prod_obj = Product.objects.get(id=obj.id)
            if product_gallery_files:
                for file in product_gallery_files:
                    ProductGalleryImage(user_id=request.user.id, product_id=prod_obj.id, product_gallery_image=file).save()
            # messages.info(request, f"Category {prod_obj.product_name} Successfully Applied Changes.")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductGalleryImageAdminView(admin.ModelAdmin):
    def product_name(self, obj):
        return Product.objects.get(id=obj.product_id).product_name

    def username(self, obj):
        return Product.objects.get(id=obj.product_id).product_name

    def gallery_image(self, obj):
        if obj.product_gallery_image.name is not None:
            return format_html(f'<img src="{obj.product_gallery_image.url}" alt="Product Home Image" width="50" height="50">')

    list_display = ['product_name', 'username', 'gallery_image', 'created_at']
    # list_filter = ('product__product_name',)
    # search_fields = ('product__product_name', 'user__username',)
    form = ProductGalleryImageFrom

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductGalleryImageAdminView, self).get_form(request, obj, **kwargs)
        if obj and obj.product_gallery_image.name != '' and obj.product_gallery_image.name is not None:
            form.base_fields['product_gallery_image'].help_text = f'<img src="{obj.product_gallery_image.url}" alt="Product Home Image" width="80" height="80">'
        else:
            form.base_fields['product_gallery_image'].help_text = ""
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is not None:
                form.cleaned_data['user_id'] = request.user.id
                if 'product_gallery_image' in form.cleaned_data and form.cleaned_data['product_gallery_image'] is not None:
                    pgi = ProductGalleryImage.objects.get(id=obj.id)
                    pgi.product_gallery_image = form.cleaned_data.get('product_gallery_image')
                    pgi.updated_at = datetime.now()
                    pgi.save()
                elif request.POST.get('product_gallery_image-clear') == 'on':
                    obj.delete()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductSizeAdminView(admin.ModelAdmin):
    def product_name(self, obj):
        return Product.objects.get(id=obj.product_id).product_name

    def username(self, obj):
        return Product.objects.get(id=obj.product_id).product_name

    def product_size(self, obj):
        if obj.size_image.name != '' and obj.size_image.name is not None:
            return format_html(f'<img src="{obj.size_image.url}" alt="Product Size Image" width="50" height="50">')

    list_display = ['product_name', 'username', 'size', 'product_size', 'price', 'created_at']
    form = ProductSizeForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductSizeAdminView, self).get_form(request, obj, **kwargs)
        if obj.size_image.name != '' and obj.size_image.name is not None:
            form.base_fields['size_image'].help_text = f'<img src="{obj.size_image.url}" alt="Product Size Image" width="80" height="80">'
        else:
            form.base_fields['size_image'].help_text = ""
        return form

    def save_model(self, request, obj, form, change):
        try:

            form.cleaned_data['user_id'] = request.user.id
            if obj.id is None:
                ProductSize(**form.cleaned_data).save()
            else:
                if 'size_image' in form.cleaned_data and form.cleaned_data['size_image'] and form.cleaned_data['size_image'] != '':
                    prod_obj = ProductSize.objects.get(id=obj.id)
                    prod_obj.size_image = form.cleaned_data['size_image']
                    prod_obj.save()
                    del form.cleaned_data['size_image']
                ProductSize.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Product Size saved")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductCanvasAdminView(admin.ModelAdmin):
    def product_name(self, obj):
        return Product.objects.get(id=obj.product_id).product_name

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    def product_canvas(self, obj):
        if obj.canvas_image.name is not None:
            return format_html(f'<img src="{obj.canvas_image.url}" alt="Product Canvas Image" width="50" height="50">')

    list_display = ['product_name', 'username', 'canvas', 'product_canvas', 'price', 'created_at']
    form = ProductCanvasForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductCanvasAdminView, self).get_form(request, obj, **kwargs)
        if obj and obj.canvas_image.name != '' and obj.canvas_image.name is not None:
            form.base_fields['canvas_image'].help_text = f'<img src="{obj.canvas_image.url}" alt="Product Canvas Image" width="80" height="80">'
        else:
            form.base_fields['canvas_image'].help_text = ""

        return form

    def save_model(self, request, obj, form, change):
        try:
            form.cleaned_data['user_id'] = request.user.id
            if obj.id is None:
                ProductCanvas(**form.cleaned_data).save()
            else:
                if 'canvas_image' in form.cleaned_data and form.cleaned_data['canvas_image'] and form.cleaned_data['canvas_image'] != '':
                    prod_obj = ProductCanvas.objects.get(id=obj.id)
                    prod_obj.canvas_image = form.cleaned_data['canvas_image']
                    prod_obj.save()
                    del form.cleaned_data['canvas_image']
                ProductCanvas.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Product Size saved")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(Product, ProductAdminView)
admin.site.register(ProductGalleryImage, ProductGalleryImageAdminView)
admin.site.register(ProductSize, ProductSizeAdminView)
admin.site.register(ProductCanvas, ProductCanvasAdminView)

