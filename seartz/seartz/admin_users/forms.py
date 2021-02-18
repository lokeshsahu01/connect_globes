from django import forms
from .models import *
from random import randint
from django.contrib.auth.hashers import make_password
import os, sys


class UserRoleChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.role}'


class UserDepartmentChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.department}'


class SubUserChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.first_name + " " + obj.last_name}'


class AdminUsersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AdminUsersForm, self).__init__(*args, **kwargs)
        for i in range(5):
            self.rand_id = randint(10 ** (8 - 1), (10 ** 8) - 1)
            if not User.objects.filter(account_id=self.rand_id).exists():
                self.fields['account_id'] = forms.CharField(required=True,
                                                            widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                                            initial=self.rand_id)
                break
            else:
                continue

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(required=True, initial='+91')
    user_role = UserRoleChoiceField(queryset=UserRole.objects.all(), required=True)
    user_department = UserDepartmentChoiceField(queryset=UserDepartment.objects.all(), required=True)
    sub_user = SubUserChoiceField(queryset=User.objects.all(), required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('account_id', 'first_name', 'last_name', 'email', 'mobile', 'user_role',
                  'user_department', 'sub_user', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super(AdminUsersForm, self).clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password And Confirm Password Not Match")
        else:
            cleaned_data['password'] = make_password(cleaned_data['password'])
            cleaned_data['user_role'] = cleaned_data['user_role'].id
            cleaned_data['user_department'] = cleaned_data['user_department'].id
            if 'sub_user' in cleaned_data and cleaned_data['sub_user'] is not None:
                cleaned_data['sub_user'] = cleaned_data['sub_user'].id


class UserLoginForm(forms.Form):
    mobile = forms.CharField(required=True)
    password = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('mobile', 'password')

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        if not User.objects.filter(mobile=cleaned_data['mobile']).exists():
            raise forms.ValidationError("You are not registered with us. Please sign up.")
        else:
            if not User.objects.get(mobile=cleaned_data['mobile']).check_password(cleaned_data['password']):
                raise forms.ValidationError("Your mobile or password is incorrect")
        return cleaned_data


class UserChangePasswordsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserChangePasswordsForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(required=True, widget=forms.PasswordInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super(UserChangePasswordsForm, self).clean()
        if not self.request.user.check_password(cleaned_data['old_password']):
            raise forms.ValidationError("Password Is Incorrect !!!")
        else:
            if cleaned_data['password'] != cleaned_data['confirm_password']:
                raise forms.ValidationError("Password And Confirm Password Not Match")
        return cleaned_data


class LoginOTPSendForm(forms.Form):
    mobile = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('mobile', )

    def clean(self):
        cleaned_data = super(LoginOTPSendForm, self).clean()
        return cleaned_data


class LoginOTPVerifyForm(forms.Form):
    mobile = forms.CharField(required=True)
    otp = forms.CharField(required=True)
    password = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('mobile', 'otp', 'password')

    def clean(self):
        cleaned_data = super(LoginOTPVerifyForm, self).clean()
        if cleaned_data['password'] is None or cleaned_data['password'] == '':
            if not User.objects.filter(mobile=cleaned_data['mobile']).exists():
                raise forms.ValidationError("Your mobile or password is incorrect")
        return cleaned_data


class CreateArtistJuniorForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    dob = forms.DateField(required=True, input_formats=['%Y/%m/%d'])
    age_proof_id = forms.CharField(required=True)
    age_proof_id_no = forms.CharField(required=False)
    age_proof_id_file = forms.FileField(required=False)
    user_image = forms.FileField(required=False)
    profile_description = forms.CharField(required=False, widget=forms.Textarea())
    address = forms.CharField(required=False, widget=forms.Textarea())
    father_name = forms.CharField(required=False)

    class Meta:
        model = ArtistJuniorProfile
        fields = ('dob', 'age_proof_id', 'age_proof_id_no', 'age_proof_id_file', 'user_image',
                  'profile_description', 'first_name', 'last_name', 'address', 'father_name')

    def clean(self):
        cleaned_data = super(CreateArtistJuniorForm, self).clean()
        return cleaned_data


class ArtistLoginOTPVerifyForm(forms.Form):
    mobile = forms.CharField(required=True)
    otp = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    dob = forms.DateField(required=False, input_formats=['%Y/%m/%d'])
    age_proof_id = forms.CharField(required=False)
    age_proof_id_no = forms.CharField(required=False)
    age_proof_id_file = forms.FileField(required=False)
    user_image = forms.FileField(required=False)
    profile_description = forms.CharField(required=False, widget=forms.Textarea())
    address = forms.CharField(required=False, widget=forms.Textarea())
    father_name = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = ArtistJuniorProfile
        fields = ('mobile', 'otp', 'email', 'first_name', 'last_name', 'dob', 'age_proof_id', 'age_proof_id_no', 'age_proof_id_file', 'user_image',
                  'profile_description', 'password', 'address', 'father_name')

    def clean(self):
        cleaned_data = super(ArtistLoginOTPVerifyForm, self).clean()
        return cleaned_data
