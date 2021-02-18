from django.db import models
from django.utils.safestring import mark_safe
from random import randint
import os


class CompanyUser(models.Model):
    password = models.CharField(max_length=250)
    is_login = models.BooleanField(default=False)
    last_login = models.DateField(null=True, blank=True)
    username = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    is_company = models.BooleanField(default=False)
    company_sub_user_id = models.ForeignKey('CompanyUser', on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='company_sub_user')
    key = models.CharField(max_length=250, null=True, blank=True)
    account_id = models.IntegerField(unique=True, default=randint(10**(8-1), (10**8)-1))
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)


class CompanyDetails(models.Model):
    def folder_path(self, filename):
        if self.user.is_company:
            upload_dir = os.path.join('plr/', str(self.user.username)+'/'+'images/')
            return os.path.join(upload_dir, filename)

    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE,
                             verbose_name='Company Primary User Name')
    enterprise_id = models.CharField(max_length=200, verbose_name='Enterprise ID')
    company_name = models.CharField(max_length=255, verbose_name='Company Name')
    company_address = models.TextField(max_length=500, verbose_name='Company Address')
    company_contact = models.CharField(max_length=200, verbose_name='Company Contact')
    company_pan = models.CharField(max_length=255, verbose_name='Company PAN')
    company_gstn = models.CharField(max_length=255, verbose_name='Company GSTN', blank=True)

    owner_name = models.CharField(max_length=255, default='', verbose_name='Company Primary admin Name')
    company_primary_email = models.EmailField(max_length=255, default='', unique=True,
                                              verbose_name='Company Primary Email- ID')
    company_primary_mobile = models.CharField(max_length=200, default='', unique=True,
                                              verbose_name='Company Primary Mobile')
    allowed_user = models.IntegerField(default=0, verbose_name='No. of users required')
    allowed_space = models.IntegerField(choices=[(5, '5 GB'), (10, '10 GB'), (15, '15 GB'), (20, '20 GB')], default=0,
                                        verbose_name='Space required')
    company_image = models.FileField(upload_to=folder_path, default='')
    allow_scanning = models.CharField(max_length=2, choices=[('t', 'Yes'), ('f', 'No')], default='f',
                                      verbose_name='Scanning required')
    estimate_page = models.IntegerField(default=0, verbose_name='Estimated pages')
    status = models.BooleanField(default=True)
    subscription = models.CharField(max_length=8, choices=[('DMS', 'DMS'), ('TMS', 'TMS'), ('BOTH', 'BOTH')])
    subscription_duration = models.CharField(max_length=8, choices=[('0', 'Free trial'), ('1', 'year'), ('2', 'years')])
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Companies"

    def image_tag(self):

        if self.company_image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.company_image.url)
        else:
            return 'no image found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.company_name


class UserLevels(models.Model):
    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE, related_name="company_user")
    level_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserDepartment(models.Model):
    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class CompanySubUser(models.Model):
    def folder_path(self, filename):
        if not self.user.is_company:
            upload_dir = os.path.join('plr/',
                                      str(self.user.company_sub_user_id.username)+'/'+str(self.user.username)+'/'+'images/')
            return os.path.join(upload_dir, filename)

    user = models.ForeignKey('CompanyUser', on_delete=models.CASCADE, related_name='user_profile')
    company_id = models.ForeignKey('CompanyUser', on_delete=models.CASCADE, related_name='company_id')
    user_level = models.ForeignKey(UserLevels, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='', unique=True)
    phone = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=50, default='', null=True, blank=True)
    location = models.TextField(max_length=1000, default='')
    user_image = models.FileField(upload_to=folder_path, default='')
    user_in_under = models.ForeignKey('CompanyUser', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='user_in_under')
    pub_date = models.DateTimeField('Create Date', auto_now_add=True)
    is_deactivate = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=[('T', 'Live'), ('F', 'Not live')], default='T')
    user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

