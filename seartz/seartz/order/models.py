from djongo import models
from admin_users.models import User
from product.models import Product
from admin_users.models import User
import os, sys
from datetime import datetime


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=250)
    product_id = models.CharField(max_length=250)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class OrderAddress(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=250)
    pin_code = models.IntegerField()
    address = models.TextField(max_length=20000)
    landmark = models.CharField(max_length=250, null=True, blank=True)
    town_city = models.CharField(max_length=250)
    State = models.CharField(max_length=250)
    address_type = models.CharField(max_length=250)
    is_default = models.BooleanField(default=False)
    is_select = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class CouponCode(models.Model):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('CouponCode/', f'{year}/{month}/{date}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=250)
    coupon_discount_amount = models.FloatField(default=0)
    coupon_discount_percentage = models.FloatField(default=0)
    coupon_image = models.FileField(upload_to=folder_path)
    is_valid = models.BooleanField(default=True)
    coupon_description = models.TextField(max_length=20000, null=True, blank=True)
    valid_for = models.TextField(max_length=20000, null=True, blank=True)
    valid_for_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = CouponCode.objects.last().id + 1 if CouponCode.objects.last() else 1
        super(CouponCode, self).save(*args, **kwargs)


class LIstField(models.Field):
    product_id = models.CharField(max_length=250)
    seller_id = models.CharField(max_length=250)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    delivery_charge = models.IntegerField()
    status = models.CharField(max_length=250)
    shipping_address = models.TextField(max_length=2000, null=True, blank=True)


class Order(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user_id = models.CharField(max_length=250)
    product = LIstField()
    order_address_id = models.CharField(max_length=250)
    order_id = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    coupon_code_id = models.CharField(max_length=250)
    coupon_discount = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=250)
    delivery_charge = models.IntegerField()
    delivery_status = models.CharField(max_length=250, null=True, blank=True)
    payment_method = models.CharField(max_length=20)
    razorpay_payment_id = models.CharField(max_length=250, null=True, blank=True)
    payment_status = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Order.objects.last().id + 1 if Order.objects.last() else 1
        super(Order, self).save(*args, **kwargs)


