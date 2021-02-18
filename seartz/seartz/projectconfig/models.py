from djongo import models
import os
from datetime import datetime


class HomeSlider(models.Model):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('HomeSlider/', f'{year}/{month}/{date}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=250)
    slider_image = models.FileField(upload_to=folder_path)
    is_featured = models.BooleanField(default=False)
    featured_user_id = models.CharField(max_length=250)
    description = models.TextField(max_length=65500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = HomeSlider.objects.last().id + 1 if HomeSlider.objects.last() else 1
        super(HomeSlider, self).save(*args, **kwargs)


class GalleryCategory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    category_name = models.CharField(max_length=250, unique=True)
    status = models.BooleanField(default=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = GalleryCategory.objects.last().id + 1 if GalleryCategory.objects.last() else 1
        super(GalleryCategory, self).save(*args, **kwargs)


class Gallery(models.Model):
    def folder_path(self, filename):
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        upload_dir = os.path.join('Gallery/', f'{year}/{month}/{date}')
        return os.path.join(upload_dir, filename)

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    category_id = models.IntegerField()
    image_name = models.CharField(max_length=250)
    image_size = models.CharField(max_length=250)
    image = models.FileField(upload_to=folder_path)
    alt = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Gallery.objects.last().id + 1 if Gallery.objects.last() else 1
        super(Gallery, self).save(*args, **kwargs)


class SocialMediaIcon(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    icon_name = models.CharField(max_length=255, unique=True)
    icon_class = models.CharField(max_length=255)
    icon_url = models.URLField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = SocialMediaIcon.objects.last().id + 1 if SocialMediaIcon.objects.last() else 1
        super(SocialMediaIcon, self).save(*args, **kwargs)


class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    email = models.EmailField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Newsletter.objects.last().id + 1 if Newsletter.objects.last() else 1
        super(Newsletter, self).save(*args, **kwargs)


class Copyright(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    content = models.TextField(max_length=65500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Copyright.objects.last().id + 1 if Copyright.objects.last() else 1
        super(Copyright, self).save(*args, **kwargs)


class ContactUsFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    message = models.TextField(max_length=65500, null=True, blank=True)
    query_type = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = ContactUsFormModel.objects.last().id + 1 if ContactUsFormModel.objects.last() else 1
        super(ContactUsFormModel, self).save(*args, **kwargs)


class ContactUsContent(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    banner_image = models.FileField(upload_to='ContactUs/', null=True, blank=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = ContactUsContent.objects.last().id + 1 if ContactUsContent.objects.last() else 1
        super(ContactUsContent, self).save(*args, **kwargs)


class ContactUsIcons(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    contact_us_content = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    icon_class = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = ContactUsIcons.objects.last().id + 1 if ContactUsIcons.objects.last() else 1
        super(ContactUsIcons, self).save(*args, **kwargs)


class TermsAndConditions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    banner_image = models.FileField(upload_to='TermsAndConditions/', null=True, blank=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = TermsAndConditions.objects.last().id + 1 if TermsAndConditions.objects.last() else 1
        super(TermsAndConditions, self).save(*args, **kwargs)


class PrivacyAndPolicy(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    banner_image = models.FileField(upload_to='PrivacyAndPolicy/', null=True, blank=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = PrivacyAndPolicy.objects.last().id + 1 if PrivacyAndPolicy.objects.last() else 1
        super(PrivacyAndPolicy, self).save(*args, **kwargs)


class AboutUs(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    banner_image = models.FileField(upload_to='AboutUs/', null=True, blank=True, max_length=255)
    alt = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = AboutUs.objects.last().id + 1 if AboutUs.objects.last() else 1
        super(AboutUs, self).save(*args, **kwargs)


class Testimonial(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=255, unique=True)
    banner_image = models.FileField(upload_to='Testimonial/', null=True, blank=True, max_length=255)
    banner_image_alt = models.CharField(max_length=250, blank=True, null=True)
    profile_image = models.FileField(upload_to='Testimonial/', null=True, blank=True, max_length=255)
    profile_image_alt = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(max_length=10000)
    designation = models.CharField(max_length=250, blank=True, null=True)
    duration = models.CharField(max_length=250, blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)
    social_link = models.URLField(max_length=255, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = Testimonial.objects.last().id + 1 if Testimonial.objects.last() else 1
        super(Testimonial, self).save(*args, **kwargs)
