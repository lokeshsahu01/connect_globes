from rest_framework import serializers
from .models import *


class CompanyUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = CompanyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_company', 'company_sub_user_id',
                  'account_id']


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ['user', 'enterprise_id', 'company_name', 'company_address', 'company_contact', 'company_pan',
                  'company_gstn', 'owner_name', 'company_primary_email', 'company_primary_mobile', 'allowed_user',
                  'allowed_space', 'company_image', 'allow_scanning', 'estimate_page', 'subscription',
                  'subscription_duration']


class SubUserCompanyDetailsSerializer(serializers.ModelSerializer):
    user_image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CompanySubUser
        fields = ['user', 'username', 'name', 'email', 'phone', 'user_in_under', 'user_level',
                  'location', 'user_department', 'company_id', 'user_image']


class UserLevelsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLevels
        fields = '__all__'


class UserDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDepartment
        fields = '__all__'


