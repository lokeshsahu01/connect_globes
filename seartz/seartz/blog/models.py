from djongo import models
from admin_users.models import User
import os
from datetime import datetime


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    content = models.CharField(max_length=250)
    status = models.CharField(max_length=250, choices=[('Published', 'Published'), ('Publish Review', 'Publish Review'), ('Draft', 'Draft'), ('Post', 'Post')])
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    view = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    total_comment = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class BlogImage(models.Model):
    def folder_path(self, filename):
        self.username = User.objects.get(id=self.user_id).username
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Blog/', f'{year}/{month}/{date}/{self.username}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    blog_id = models.IntegerField()
    user_id = models.IntegerField()
    blog_image = models.FileField(upload_to=folder_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class BlogHeart(models.Model):
    id = models.AutoField(primary_key=True)
    blog_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class BlogView(models.Model):
    id = models.AutoField(primary_key=True)
    blog_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class BlogComment(models.Model):
    blog_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    comment = models.TextField(max_length=65500)
    sub_comment = models.CharField(max_length=250, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=250, null=True, blank=True)
    unapproved_by = models.CharField(max_length=250, null=True, blank=True)
    reject_reason = models.TextField(max_length=65000, null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class BlogCommentLike(models.Model):
    user_id = models.CharField(max_length=250)
    blog_id = models.CharField(max_length=250)
    blog_comment_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
