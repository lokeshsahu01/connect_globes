from admin_users.models import User
from categories.models import *
from django.db import models
import os
from datetime import datetime
from datetime import date
from location.models import *


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='shipping_address_country_name')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shipping_address_city_name')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='shipping_address_state_name')
    pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE, related_name='shipping_address_pincode')
    address = models.TextField(max_length=20000)
    landmark = models.CharField(max_length=250, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Brand(models.Model):
    def folder_path(self, filename):
        upload_dir = os.path.join('brand/', f'{self.brand_name}')
        return os.path.join(upload_dir, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_user')
    brand_name = models.CharField(max_length=250)
    is_feature = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    brand_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    alt = models.TextField(max_length=50000, null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='brand_approved_by_user')
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    def folder_path(self, filename):
        product_name = self.product_name.lower().replace(' ', '_')
        upload_dir = os.path.join('products/', f'{product_name}/certificate')
        return os.path.join(upload_dir, filename)

    product_code = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_user')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='product_brand_relation')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=255, unique=True)
    product_description = models.TextField(max_length=65500, null=True, blank=True)
    product_specification = models.TextField(max_length=65500, null=True, blank=True)
    purchase_note = models.TextField(max_length=65500, null=True, blank=True)
    certificate_by = models.CharField(max_length=250, null=True, blank=True)
    certificate_file = models.FileField(upload_to=folder_path, blank=True, null=True)
    price = models.FloatField(max_length=250)
    selling_price = models.FloatField(max_length=250)
    price_off = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    total_comment = models.IntegerField(default=0)
    total_review = models.FloatField(default=0)
    is_feature = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('admin_users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='product_approved_by_user')
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    delivery_charge = models.IntegerField(default=0)
    is_cod = models.BooleanField(default=True)
    product_tags = models.TextField(max_length=65500, null=True, blank=True)
    delivery_time = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_keeping_unit = models.CharField(max_length=250)
    stock_quantity = models.IntegerField(default=0)
    stock_status = models.CharField(max_length=250, choices=(('In stock', 'In stock'), ('Out of stock', 'Out of stock'), ('On backorder', 'On backorder')), null=True, blank=True)
    allow_backorders = models.CharField(max_length=250, choices=(('Do not allow', 'Do not allow'), ('Allow, but notify customer', 'Allow, but notify customer'), ('Allow', 'Allow')), null=True, blank=True)
    low_stock_threshold = models.IntegerField(default=0)
    sold_individually = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductShipping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.CharField(max_length=250)
    length = models.CharField(max_length=250)
    width = models.CharField(max_length=250)
    height = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductGalleryImage(models.Model):
    def folder_path(self, filename):
        product_name = self.product.product_name.lower().replace(' ', '_')
        upload_dir = os.path.join('products/', f'{product_name}/images')
        return os.path.join(upload_dir, filename)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_gallery_image = models.FileField(upload_to=folder_path, blank=True, null=True, max_length=255)
    alt = models.TextField(max_length=10000, null=True, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductGalleryVideo(models.Model):
    def folder_path(self, filename):
        product_name = self.product.product_name.lower().replace(' ', '_')
        upload_dir = os.path.join('products/', f'{product_name}/videos')
        return os.path.join(upload_dir, filename)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_gallery_video = models.FileField(upload_to=folder_path, blank=True, null=True, max_length=255)
    alt = models.TextField(max_length=10000, null=True, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductSize(models.Model):
    def folder_path(self, filename):
        product_name = self.product.product_name.lower().replace(' ', '_')
        upload_dir = os.path.join('products/', f'{product_name}/sizes')
        return os.path.join(upload_dir, filename)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(max_length=250)
    size_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    alt = models.TextField(max_length=10000, null=True, blank=True)
    is_feature = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color_code = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_comment_user")
    comment = models.TextField(max_length=65500)
    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='product_sub_comment', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('admin_users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='product_comment_approved_by_user')
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.IntegerField(default=1)
    review_description = models.TextField(max_length=65500, null=True, blank=True)
    approved_by = models.ForeignKey('admin_users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='product_review_approved_by_user')
    is_approved = models.BooleanField(default=False)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
