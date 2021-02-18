from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from datetime import datetime
from .managers import *


class UserRole(models.Model):
    role = models.CharField(max_length=250, unique=True)
    is_create_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserDepartment(models.Model):
    department = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    username = None
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=13, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    account_id = models.IntegerField(unique=True)
    is_email = models.BooleanField(default=False)
    token = models.TextField(max_length=20000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    sub_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = ['user_role', 'user_department', 'updated_at', 'account_id', 'sub_user',
                       'first_name', 'last_name', 'is_mobile', 'is_email', 'token']

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile

    class Meta:
        verbose_name_plural = "User"


class UserProfile(models.Model):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('UserImages/', f'{year}/{month}/{date}/{self.user.username}')
        return os.path.join(upload_dir, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_image = models.FileField(upload_to=folder_path, null=True, blank=True)
    alt = models.TextField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=250)
    State = models.CharField(max_length=250)
    pin_code = models.IntegerField()
    address = models.TextField(max_length=20000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
