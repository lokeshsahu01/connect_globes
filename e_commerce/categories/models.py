from admin_users.models import *
import os
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Category/', f'{year}/{month}/{date}')
        return os.path.join(upload_dir, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=250, unique=True)
    status = models.BooleanField(default=True)
    category_image = models.FileField(upload_to=folder_path, null=True, blank=True)
    alt = models.TextField(max_length=1000, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category_description = models.TextField(max_length=10000, null=True, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
