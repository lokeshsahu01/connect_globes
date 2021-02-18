from djongo import models
import os
# Create your models here.
from datetime import datetime
from datetime import date


class Categories(models.Model):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Category/', f'{year}/{month}/{date}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=250, unique=True)
    status = models.CharField(max_length=250, choices=[('Inactive', 'Inactive'), ('Active', 'Active')])
    category_image = models.FileField(upload_to=folder_path, null=True, blank=True)
    sub_category = models.IntegerField(null=True, blank=True)
    category_description = models.TextField(max_length=10000, null=True, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

