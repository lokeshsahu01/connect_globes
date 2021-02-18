from django import forms
from .models import *
from random import randint
from django.contrib.auth.hashers import make_password


class UserRoleChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.role}'


class UserDepartmentChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.department}'


class SubUserChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.username}'


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
    username = forms.CharField(required=True)
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
        fields = ('account_id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'user_role',
                  'user_department', 'sub_user', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super(AdminUsersForm, self).clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password And Confirm Password Not Match")
        else:
            cleaned_data['password'] = make_password(cleaned_data['password'])
            cleaned_data.pop('confirm_password')
        cleaned_data['is_staff'] = True
        cleaned_data['is_active'] = True
        return cleaned_data
