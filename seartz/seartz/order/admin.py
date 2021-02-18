from django.contrib import admin
from .models import *
from admin_users.models import *
from product.models import *
from django.contrib import messages
from .forms import *
from django.utils.html import format_html, mark_safe


class CouponCodeeAdminView(admin.ModelAdmin):
    list_display = ['coupon_code', 'coupon_discount_amount', 'coupon_discount_percentage', 'is_valid', 'valid_for_amount', 'created_at']
    form = CouponCodeeForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                CouponCode(**form.cleaned_data).save()
            else:
                CouponCode.objects.filter(id=obj.id).update(**form.cleaned_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class OrderAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def user(self, obj):
        return User.objects.get(id=obj.user_id).username

    def coupon_code(self, obj):
        if obj.coupon_code_id:
            return CouponCode.objects.get(id=obj.coupon_code_id).coupon_code

    def products(self, obj):
        html = ""
        for i in obj.product:
            html += f'''<a href="/admin/product/product/{i['product_id']}/change/">{i['product_id']}</a> | '''
        return format_html(html)

    list_display = ['id', 'order_id', 'user',  'quantity', 'products', 'price', 'coupon_code', 'coupon_discount', 'total_price', 'status', 'delivery_charge',
                    'delivery_status', 'payment_method', 'razorpay_payment_id', 'payment_status', 'created_at']


admin.site.register(CouponCode, CouponCodeeAdminView)
admin.site.register(Order, OrderAdminView)
