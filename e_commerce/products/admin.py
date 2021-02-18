from django.contrib import admin
from .models import *
from .forms import *
from django.utils.html import format_html
from django.contrib import messages
import os, sys


class ProductAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def category_name(self, obj):
        html = f'''<a href="/admin/categories/categories/{obj.category.id}/change/">{obj.category.category_name}</a>'''
        return format_html(html)

    def url(self, obj):
        html = f'''<a href="http://paperlessrack.in/detailpage/{obj.slug}">{obj.slug}</a>'''
        return format_html(html)

    def status_change(self, obj):
        return format_html(f'''<a href="/api/v1/products/status/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.status else 'no'}.svg" alt="True"></a>''')

    def feature(self, obj):
        return format_html(f'''<a href="/api/v1/products/feature/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_feature else 'no'}.svg" alt="True"></a>''')

    def approved(self, obj):
        return format_html(f'''<a href="/api/v1/products/approve/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_approved else 'no'}.svg" alt="True"></a>''')

    def product_price(self, obj):
        if obj.selling_price == 0 or obj.selling_price is None or obj.selling_price == '':
            return obj.price
        else:
            return obj.selling_price

    def approved_by_user(self, obj):
        if obj.approved_by:
            return obj.approved_by.username

    def product(self, obj):
        if ProductGalleryImage.objects.filter(product=obj):
            html = f'''<a href="/admin/products/productgalleryimage/?product__id={obj.id}">{obj.product_name}</a>'''
        else:
            html = obj.product_name
        return format_html(html)
    list_display = ['product_code', 'product', 'user', 'category_name', 'product_price', 'status_change', 'feature', 'approved', 'approved_by_user', 'slug', 'delivery_charge',
                    'is_cod', 'created_at']
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
            if ProductGalleryImage.objects.filter(product=obj).exists():
                filename = " "
                for i in ProductGalleryImage.objects.filter(product=obj):
                    filename += f'''<a href="/admin/products/productgalleryimage/{i.product.id}/change/">
                                        <img src="{i.product_gallery_image.url}" alt="Product Gallery Image" width="50" height="50" style="padding:5px">
                                    </a>'''
                form.base_fields['product_gallery_image'].help_text = filename
        return form

    def save_model(self, request, obj, form, change):
        try:
            product_gallery_files = None
            product_gallery_video = None
            if 'product_gallery_image' in request.FILES and request.FILES['product_gallery_image'] is not None:
                product_gallery_files = request.FILES.getlist('product_gallery_image')
            if 'product_gallery_image' in form.cleaned_data:
                del form.cleaned_data['product_gallery_image']
            if 'product_gallery_video' in request.FILES and request.FILES['product_gallery_video'] is not None:
                product_gallery_video = request.FILES.getlist('product_gallery_video')
            if 'product_gallery_video' in form.cleaned_data:
                del form.cleaned_data['product_gallery_video']
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                Product(**form.cleaned_data).save()
                prod_obj = Product.objects.last()
            else:
                Product.objects.filter(id=obj.id).update(**form.cleaned_data)
                prod_obj = Product.objects.get(id=obj.id)
            if product_gallery_files:
                for file in product_gallery_files:
                    ProductGalleryImage(user=User.objects.get(id=request.user.id), product=prod_obj, alt=file.name, product_gallery_image=file).save()
            if product_gallery_video:
                for video in product_gallery_video:
                    ProductGalleryVideo(user=User.objects.get(id=request.user.id), product=prod_obj, alt=video.name, product_gallery_video=video).save()
            messages.info(request, f"Category {prod_obj.product_name} Successfully Applied Changes.")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductGalleryImageAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def product_name(self, obj):
        return obj.product.product_name

    def feature(self, obj):
        return format_html(f'''<a href="/api/v1/products/gallery/image/feature/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_feature else 'no'}.svg" alt="True"></a>''')

    list_display = ['id', 'product_name', 'username', 'feature', 'created_at']
    search_fields = ('id', 'product__product_name', 'user__username')


class ProductSizeAdminView(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'product_name', 'username', 'size', 'price', 'created_at']
    form = ProductSizeForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductSizeAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if 'size_image' in form.base_fields and obj.size_image.name:
                filename = f'''<img src="{obj.size_image.url}" alt="Product Size Image" width="400" height="120" style="padding:5px">'''
                form.base_fields['size_image'].help_text = filename
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                ProductSize(**form.cleaned_data).save()
            else:
                if 'size_image' in form.cleaned_data and form.cleaned_data['size_image']:
                    prod_size = ProductSize.objects.get(id=obj.id)
                    prod_size.size_image = form.cleaned_data['size_image']
                    prod_size.alt = form.cleaned_data['alt']
                    prod_size.save()
                    form.cleaned_data.pop('size_image')
                    form.cleaned_data.pop('alt')
                form.cleaned_data['updated_at'] = datetime.now()
                ProductSize.objects.filter(id=obj.id).update(**form.cleaned_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ShippingAddressAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def country_name(self, obj):
        return obj.country.country_name

    def state_name(self, obj):
        return obj.state.state_name

    def city_name(self, obj):
        return obj.city.city_name

    def pin_code(self, obj):
        return obj.pincode.pincode

    list_display = ['id', 'user', 'full_name', 'mobile_number', 'country_name', 'state_name', 'city_name', 'pin_code', 'address', 'is_default', 'created_at']
    form = ShippingAddressForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=self.request.user.id)
                ShippingAddress(**form.cleaned_data).save()
            else:
                ShippingAddress.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Shipping Address")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class BrandAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'user', 'brand_name', 'is_feature', 'is_approved', 'approved_by', 'created_at']
    form = BrandForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(BrandAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if 'brand_image' in form.base_fields and obj.brand_image.name:
                filename = f'''<img src="{obj.brand_image.url}" alt="Brand Size Image" width="400" height="120" style="padding:5px">'''
                form.base_fields['brand_image'].help_text = filename
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                if 'is_approved' in form.cleaned_data and form.cleaned_data['is_approved']:
                    form.cleaned_data['approved_by'] = User.objects.get(id=request.user.id)
                Brand(**form.cleaned_data).save()
            else:
                if 'brand_image' in form.cleaned_data and form.cleaned_data['brand_image']:
                    brand_obj = Brand.objects.get(id=obj.id)
                    brand_obj.brand_image = form.cleaned_data['brand_image']
                    brand_obj.save()
                    form.cleaned_data.pop('brand_image')
                form.cleaned_data['updated_at'] = datetime.now()
                Brand.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, f"Successfully Applied Changes on Brand {obj.brand_name}")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductInventoryAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id', 'username', 'product_name', 'stock_keeping_unit', 'stock_quantity', 'stock_status', 'allow_backorders', 'low_stock_threshold', 'sold_individually', 'created_at']
    form = ProductInventoryForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                ProductInventory(**form.cleaned_data).save()
            else:
                ProductInventory.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Product Inventory ")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductShippingAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id',  'username', 'product_name', 'weight', 'length', 'width', 'height', 'created_at']
    form = ProductShippingForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                ProductShipping(**form.cleaned_data).save()
            else:
                ProductShipping.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Product Shipping")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductGalleryVideoAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def product_name(self, obj):
        return obj.product.product_name

    def feature(self, obj):
        return format_html(f'''<a href="/api/v1/products/gallery/video/feature/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_feature else 'no'}.svg" alt="True"></a>''')

    list_display = ['id',  'username', 'product_name', 'feature', 'created_at']
    search_fields = ('id', 'product__product_name', 'user__username')


class ProductColorAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id',  'username', 'product_name', 'color_code', 'created_at']
    form = ProductColorForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                ProductColor(**form.cleaned_data).save()
            else:
                ProductColor.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Product Color")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductCommentAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def username(self, obj):
        return obj.user.username

    list_display = ['id',  'user', 'product', 'comment', 'sub_comment', 'is_approved', 'approved_by', 'is_feature', 'created_at']


class ProductReviewAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def username(self, obj):
        return obj.user.username

    list_display = ['id',  'user', 'product', 'review', 'is_feature', 'is_approved', 'approved_by', 'created_at']


admin.site.register(ShippingAddress, ShippingAddressAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Product, ProductAdminView)
admin.site.register(ProductInventory, ProductInventoryAdminView)
admin.site.register(ProductShipping, ProductShippingAdminView)
admin.site.register(ProductGalleryImage, ProductGalleryImageAdminView)
admin.site.register(ProductGalleryVideo, ProductGalleryVideoAdminView)
admin.site.register(ProductSize, ProductSizeAdminView)
admin.site.register(ProductColor, ProductColorAdminView)
admin.site.register(ProductComment, ProductCommentAdminView)
admin.site.register(ProductReview, ProductReviewAdminView)
