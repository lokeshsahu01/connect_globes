from django.db import models
import os


class Country(models.Model):
    country_name = models.CharField(max_length=250, unique=True)
    country_code = models.CharField(max_length=250, null=True, blank=True)
    country_currency = models.CharField(max_length=250, null=True, blank=True)
    country_phone_code = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class State(models.Model):
    def folder_path(self, filename):
        upload_dir = os.path.join('State/', f'{self.state_name}')
        return os.path.join(upload_dir, filename)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='state_country_name')
    state_name = models.CharField(max_length=250, unique=True)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=250)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    state_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    alt = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class City(models.Model):
    def folder_path(self, filename):
        upload_dir = os.path.join('City/', f'{self.city_name}')
        return os.path.join(upload_dir, filename)

    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city_state_name')
    city_name = models.CharField(max_length=250, unique=True)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=250)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    city_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    alt = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Pincode(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='pincode_state_name')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pincode_city_name')
    pincode = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)