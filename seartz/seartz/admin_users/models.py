from djongo import models
from django.contrib.auth.models import AbstractUser
import os
from datetime import datetime
from .managers import *


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=250, unique=True)
    is_create_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserDepartment(models.Model):
    department = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = None
    user_role = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    user_department = models.CharField(max_length=250, null=True, blank=True)
    mobile = models.CharField(max_length=13, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    account_id = models.IntegerField(unique=True)
    is_email = models.BooleanField(default=False)
    token = models.TextField(max_length=20000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    sub_user = models.CharField(max_length=250, null=True, blank=True)

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = ['user_role', 'user_department', 'email', 'updated_at', 'account_id', 'sub_user',
                       'first_name', 'last_name', 'is_mobile', 'is_email', 'token']
    objects = CustomUserManager()

    def __str__(self):
        return self.mobile

    class Meta:
        verbose_name_plural = "User"


class BuyerProfile(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.TextField(max_length=10000, null=True, blank=True)
    user_id = models.CharField(max_length=250)


class ArtistJuniorProfile(models.Model):
    def folder_path(self, filename):
        self.account_id = User.objects.get(id=self.user_id).account_id
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('User/', f'{year}/{month}/{date}/{self.account_id}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=250)
    address = models.TextField(max_length=10000, null=True, blank=True)
    father_name = models.CharField(max_length=250, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    age_proof_id = models.CharField(max_length=250, null=True, blank=True)
    age_proof_id_no = models.CharField(max_length=250, null=True, blank=True)
    age_proof_id_file = models.FileField(upload_to=folder_path, null=True, blank=True)
    user_image = models.FileField(upload_to=folder_path, null=True, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    profile_description = models.TextField(max_length=65000, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class CompanyUserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=250)

