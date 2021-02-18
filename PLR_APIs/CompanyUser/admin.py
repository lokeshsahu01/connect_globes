from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from .serializers import *
from PLR_APIs.logs import *
import os
import sys
from .forms import *
import hashlib


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_id', 'username', 'email', 'is_company', 'date_joined')
    search_fields = ('CompanyUser__username', 'CompanyUser__first_name', 'CompanyUser__last_name',
                     'CompanyUser__account_id', 'CompanyUser__email')
    form = CompanyUserCreateForm

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            try:
                if form.is_valid():
                    form.cleaned_data['password'] = 'pbkdf2_sha256$180000$' + hashlib.sha256(
                        form.cleaned_data["password"].encode()).hexdigest()
                    form.cleaned_data['is_company'] = True
                    form.cleaned_data['company_sub_user_id'] = None
                    for i in range(5):
                        random = randint(10**(8-1), (10**8)-1)
                        if not CompanyUser.objects.filter(account_id=random).exists():
                            form.cleaned_data['account_id'] = random
                            break
                    serialize = CompanyUserSerializer(data=form.cleaned_data)
                    if serialize.is_valid():
                        serialize.save()
                        messages.info(request, f"{serialize.data['username']} Successfully created")
                    else:
                        messages.error(request, f"{serialize.errors}")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
                messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        return obj.user.username
    list_display = ('id', 'company_image', 'user_name', 'enterprise_id', 'company_name', 'owner_name',
                    'company_primary_email', 'company_primary_mobile', 'allowed_user', 'allowed_space', 'created_at')
    search_fields = ['CompanyDetails__user__username', 'CompanyDetails__company_name', 'CompanyDetails__enterprise_id',
                     'CompanyDetails__subscription', 'CompanyDetails__subscription_duration',
                     'CompanyDetails__company_primary_email', 'CompanyDetails__company_primary_mobile']
    form = CompanyDetailsForm

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            try:
                if form.is_valid():
                    form.cleaned_data['user'] = str(form.cleaned_data['user'].id)
                    serialize = CompanyDetailsSerializer(data=form.cleaned_data)
                    if serialize.is_valid():
                        serialize.save()
                        messages.info(request, f"{serialize.data['company_name']} Has been created Successfully")
                    else:
                        messages.error(request, f"{serialize.errors}")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
                messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


@admin.register(UserLevels)
class UserLevelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


@admin.register(UserDepartment)
class UserDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


@admin.register(CompanySubUser)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
