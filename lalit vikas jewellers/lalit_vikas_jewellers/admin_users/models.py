from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.Model):
    role = models.CharField(max_length=250)
    is_create_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserDepartment(models.Model):
    department = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name="user_role")
    user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE, related_name="user_department")
    updated_at = models.DateTimeField(auto_now=True)
    account_id = models.IntegerField(unique=True)
    mobile = models.CharField(max_length=13, null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    sub_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name="admin_sub_user")

    REQUIRED_FIELDS = ['user_role', 'user_department', 'updated_at', 'account_id', 'mobile', 'is_mobile', 'is_email',
                       'sub_user']

    class Meta:
        verbose_name_plural = "User"
