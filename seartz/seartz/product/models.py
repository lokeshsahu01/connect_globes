from admin_users.models import User
from categories.models import *
from djongo import models
import os
from datetime import datetime
from datetime import date


class Product(models.Model):
    def folder_path(self, filename):
        self.username = User.objects.get(id=self.user_id).account_id
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Product/', f'{year}/{month}/{date}/{self.username}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=250, unique=True)
    user_id = models.CharField(max_length=250)
    category_id = models.CharField(max_length=250)
    product_name = models.CharField(max_length=255, unique=True)
    product_description = models.TextField(max_length=25555, null=True, blank=True)
    product_home_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    product_specification = models.TextField(max_length=65500, null=True, blank=True)
    certificate_by = models.CharField(max_length=250, null=True, blank=True)
    certificate_file = models.FileField(upload_to=folder_path, blank=True, null=True)
    price = models.FloatField(max_length=250)
    selling_price = models.FloatField(max_length=250)
    price_off = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, choices=[('Published', 'Published'), ('Post', 'Post'), ('Draft', 'Draft')])
    likes = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    total_comment = models.IntegerField(default=0)
    total_review = models.FloatField(default=0)
    is_feature = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    available_stock = models.IntegerField(default=0)
    delivery_charge = models.IntegerField(default=0)
    is_cod = models.BooleanField(default=True)
    delivery_time = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductGalleryImage(models.Model):
    def folder_path(self, filename):
        self.username = User.objects.get(id=self.user_id).account_id
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Product/', f'{year}/{month}/{date}/{self.username}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    product_gallery_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductSize(models.Model):
    def folder_path(self, filename):
        self.username = User.objects.get(id=self.user_id).account_id
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Product/', f'{year}/{month}/{date}/{self.username}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    size = models.CharField(max_length=250)
    size_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductCanvas(models.Model):
    def folder_path(self, filename):
        self.username = User.objects.get(id=self.user_id).account_id
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Product/', f'{year}/{month}/{date}/{self.username}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    canvas = models.CharField(max_length=250)
    canvas_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductHeart(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductView(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    comment = models.TextField(max_length=65500)
    sub_comment = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductReview(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    review = models.IntegerField(default=1)
    review_description = models.TextField(max_length=65500, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
