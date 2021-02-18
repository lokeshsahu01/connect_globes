from django import forms
from .models import *
import hashlib
import sys, os
from PLR_APIs.logs import *


class UserLoginForm(forms.ModelForm):
    enterprise_id = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = CompanyUser
        fields = ('enterprise_id', 'username', 'password')

    def clean(self):
        try:
            cleaned_data = super(UserLoginForm, self).clean()
            username = cleaned_data['username']
            cleaned_data['password'] = 'pbkdf2_sha256$180000$' + hashlib.sha256(
                cleaned_data["password"].encode()).hexdigest()
            enterprise_id = cleaned_data['enterprise_id']
            if CompanyUser.objects.filter(username=username, password=cleaned_data['password']).exists():
                user = CompanyUser.objects.get(username=username, password=cleaned_data['password'])
                user = user if user.is_company else user.company_sub_user_id
                if not CompanyDetails.objects.filter(enterprise_id=enterprise_id, user=user).exists():
                    raise forms.ValidationError("Enterprise Id Not Correct")
                else:
                    if not user.is_company and  not CompanySubUser.objects.filter(is_deactivate=True, user=user).exists():
                        raise forms.ValidationError("User Is Not Active")
                    return cleaned_data
            else:
                raise forms.ValidationError("Username or Password Incorrect")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            raise forms.ValidationError(f"{e}, {f_name}, {exc_tb.tb_lineno}")


class CompanySubUserCreateForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    user_in_under = forms.CharField(required=False)
    user_level = forms.CharField(required=True)
    location = forms.CharField(required=True, widget=forms.Textarea())
    user_department = forms.CharField(required=True)
    user_image = forms.FileField(required=False)

    class Meta:
        model = CompanyUser
        fields = ('username', 'password', 'first_name', 'last_name', 'phone', 'user_in_under', 'user_level',
                  'location', 'user_department', 'user_image')

    def clean(self):
        cleaned_data = super(CompanySubUserCreateForm, self).clean()
        return cleaned_data


class CompanyUserCreateForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CompanyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super(CompanyUserCreateForm, self).clean()
        return cleaned_data


class CompanyUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.username)


class CompanyDetailsForm(forms.ModelForm):
    enterprise_id = forms.CharField(required=True)
    company_name = forms.CharField(required=True)
    company_address = forms.CharField(required=True, widget=forms.Textarea())
    company_contact = forms.CharField(required=True)
    company_pan = forms.CharField(required=True)
    company_gstn = forms.CharField(required=True)
    owner_name = forms.CharField(required=True)
    company_primary_email = forms.EmailField(required=True)
    company_primary_mobile = forms.CharField(required=True)
    allowed_user = forms.IntegerField(required=True)
    allowed_space = forms.ChoiceField(choices=[(5, '5 GB'), (10, '10 GB'), (15, '15 GB'), (20, '20 GB')], required=True)
    company_image = forms.FileField(required=True)
    allow_scanning = forms.ChoiceField(required=True, choices=[('t', 'Yes'), ('f', 'No')])
    estimate_page = forms.IntegerField(required=True)
    subscription = forms.ChoiceField(required=True, choices=[('DMS', 'DMS'), ('TMS', 'TMS'), ('BOTH', 'BOTH')])
    subscription_duration = forms.ChoiceField(required=True, choices=[(0, 'Free trial'), (1, 'year'), (2, 'years')])

    class Meta:
        model = CompanyDetails
        fields = ('user', 'enterprise_id', 'company_name', 'company_address', 'company_contact', 'company_pan',
                  'company_gstn', 'owner_name', 'company_primary_email', 'company_primary_mobile', 'allowed_user',
                  'allowed_space', 'company_image', 'allow_scanning', 'estimate_page', 'subscription',
                  'subscription_duration')

    def clean(self):
        cleaned_data = super(CompanyDetailsForm, self).clean()
        return cleaned_data


class UserLevelsCreateForm(forms.ModelForm):
    level_name = forms.CharField(required=True)
    status = forms.CharField(required=True)

    class Meta:
        model = UserLevels
        fields = ('level_name', 'status')

    def clean(self):
        cleaned_data = super(UserLevelsCreateForm, self).clean()
        return cleaned_data


class UserDepartmentForm(forms.ModelForm):
    department_name = forms.CharField(required=True)
    status = forms.CharField(required=True)

    class Meta:
        model = UserLevels
        fields = ('department_name', 'status')

    def clean(self):
        cleaned_data = super(UserDepartmentForm, self).clean()
        return cleaned_data
