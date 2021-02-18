from django.db import models
import os
from datetime import datetime
from admin_users.models import *
from products.models import *


class CouponCode(models.Model):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('CouponCode/', f'{year}/{month}/{date}')
        return os.path.join(upload_dir, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=250)
    coupon_discount_max_amount = models.FloatField(default=0)
    coupon_discount_percentage = models.FloatField(default=0)
    coupon_image = models.FileField(upload_to=folder_path)
    alt = models.TextField(max_length=1000, null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    is_feature = models.BooleanField(default=False)
    coupon_description = models.TextField(max_length=20000, null=True, blank=True)
    valid_for = models.CharField(max_length=250, null=True, blank=True)
    min_valid_amount = models.FloatField(default=0)
    max_valid_amount = models.FloatField(default=0)
    term_and_condition = models.TextField(max_length=50000, null=True, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class OrderAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='order_address_country_name')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='order_address_city_name')
    State = models.ForeignKey(State, on_delete=models.CASCADE, related_name='order_address_state_name')
    pin_code = models.ForeignKey(Pincode, on_delete=models.CASCADE, related_name='order_address_pincode')
    address = models.TextField(max_length=20000)
    landmark = models.CharField(max_length=250, null=True, blank=True)
    address_type = models.CharField(max_length=250)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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


class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    order = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='relation_order')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    buyer = models.ForeignKey('admin_users.User', on_delete=models.CASCADE, related_name='buyer_seller')
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    delivery_charge = models.IntegerField()
    status = models.CharField(max_length=250)
    shipping_address = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
