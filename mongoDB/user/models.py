from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=15, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS = ['mobile', 'updated_at']