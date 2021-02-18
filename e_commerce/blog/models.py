from django.db import models
from admin_users.models import *


class Blog(models.Model):
    def folder_path(self, filename):
        upload_dir = os.path.join('Blog/', f"{self.title.lower().replace(' ', '_')}")
        return os.path.join(upload_dir, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_user")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=65500)
    footer_content = models.TextField(max_length=65500, null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=250)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    blog_banner_image = models.FileField(upload_to=folder_path, blank=True, null=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_comment_user")
    comment = models.TextField(max_length=65500)
    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='blog_sub_comment', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('admin_users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='blog_comment_approved_by_user')
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

