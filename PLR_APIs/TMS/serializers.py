from rest_framework import serializers
from .models import *
from DMS.models import ScanFile


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TaskActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskActivityLogs
        fields = '__all__'


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'


class TaskFileManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFileManagement
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_user = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=CompanyUser.objects.all())
    assigned_to_group = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=Group.objects.all())
    user_department = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=UserDepartment.objects.all())
    document_file = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=ScanFile.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
        

class ReassignTaskSerializer(serializers.ModelSerializer):
    assigned_to_user = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=CompanyUser.objects.all())
    assigned_to_group = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=Group.objects.all())
    user_department = serializers.PrimaryKeyRelatedField(required=True, allow_null=True, queryset=UserDepartment.objects.all())

    class Meta:
        model = Task
        fields = ('assigned_type', 'assigned_to_user', 'assigned_to_group', 'user_department')

