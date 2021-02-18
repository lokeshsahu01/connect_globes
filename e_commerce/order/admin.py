from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages
import sys
from django.utils.html import format_html


class CouponCodeAdminView(admin.ModelAdmin):
    def created_by(self, obj):
        return obj.user.username

    def valid(self, obj):
        return format_html(f'''<a href="/api/v1/order/coupon/valid/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_valid else 'no'}.svg" alt="True"></a>''')

    def feature(self, obj):
        return format_html(f'''<a href="/api/v1/order/coupon/feature/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_feature else 'no'}.svg" alt="True"></a>''')

    list_display = ['created_by', 'coupon_code', 'coupon_discount_max_amount', 'coupon_discount_percentage', 'valid', 'feature', 'valid_for', 'min_valid_amount', 'max_valid_amount',
                    'created_at']
    form = CouponCodeForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(CouponCodeAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if 'coupon_image' in form.base_fields and obj.coupon_image.name:
                filename = f'''<img src="{obj.coupon_image.url}" alt="Product Size Image" width="200" height="120" style="padding:5px">'''
                form.base_fields['coupon_image'].help_text = filename
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                CouponCode(**form.cleaned_data).save()
            else:
                if 'coupon_image' in form.cleaned_data and form.cleaned_data['coupon_image']:
                    coupon_obj = CouponCode.objects.get(id=obj.id)
                    coupon_obj.coupon_image = form.cleaned_data['coupon_image']
                    coupon_obj.alt = form.cleaned_data['coupon_image']
                    coupon_obj.save()
                CouponCode.objects.filter(id=obj.id).update(**form.cleaned_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(CouponCode, CouponCodeAdminView)
