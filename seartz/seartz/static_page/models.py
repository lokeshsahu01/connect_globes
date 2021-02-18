from djongo import models
import os
from datetime import datetime


class OurTeam(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    profile_image = models.FileField(upload_to='OurTeam/', null=True, blank=True, max_length=255)
    designation = models.CharField(max_length=250, blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)
    social_link = models.URLField(max_length=255, null=True, blank=True)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = OurTeam.objects.last().id + 1 if OurTeam.objects.last() else 1
        super(OurTeam, self).save(*args, **kwargs)


class Vision(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    banner_image = models.FileField(upload_to='Vision/', null=True, blank=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Vision.objects.last().id + 1 if Vision.objects.last() else 1
        super(Vision, self).save(*args, **kwargs)


class Mission(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    banner_image = models.FileField(upload_to='Mission/', null=True, blank=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Mission.objects.last().id + 1 if Mission.objects.last() else 1
        super(Mission, self).save(*args, **kwargs)


class FAndQ(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField(max_length=65500)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = FAndQ.objects.last().id + 1 if FAndQ.objects.last() else 1
        super(FAndQ, self).save(*args, **kwargs)

