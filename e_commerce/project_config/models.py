from django.db import models
from admin_users.models import *


class SocialMediaIcon(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="social_media_icon_user")
    icon_name = models.CharField(max_length=255, unique=True)
    icon_class = models.CharField(max_length=255)
    icon_url = models.URLField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="news_letter_user", null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Copyright(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="copyright_user")
    content = models.TextField(max_length=65500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
