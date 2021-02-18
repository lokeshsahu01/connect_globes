from admin_users.models import *


class ContactUsFormModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='contact_us_form_create_user')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=65500, null=True, blank=True)
    query_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ContactUsContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="contact_us_content_user")
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


class ContactUsIcons(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="contact_us_icons_user")
    contact_us_content = models.ForeignKey(ContactUsContent, on_delete=models.CASCADE, related_name='contact_us_content')
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=65500)
    icon_class = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TermsAndConditions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="terms_and_conditions_user")
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


class PrivacyAndPolicy(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="privacy_and_policy_user")
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


class AboutUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="about_us_user")
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


class FAndQ(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="f_and_q_user")
    page = models.CharField(max_length=255)
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField(max_length=65500)
    slug = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
