from django import forms
from .models import *


class GroupForm(forms.Form):
    group_name = forms.CharField(required=True)
    selected_user_list = forms.CharField(required=True)
    group_desc = forms.CharField(required=True)

    class Meta:
        model = Group
        fields = ('group_name', 'selected_user_list', 'group_desc')

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        if 'selected_user_list' in cleaned_data and cleaned_data['selected_user_list'] is not None and cleaned_data['selected_user_list'] != '':
            selected_user = eval(cleaned_data['selected_user_list'])
            for i in selected_user:
                if not CompanyUser.objects.filter(id=i).exists():
                    raise forms.ValidationError(f"User ID {i} Not Exists !!!")
        return cleaned_data


class TaskForm(forms.Form):
    task_title = forms.CharField(required=True)
    task_description = forms.CharField(required=True, widget=forms.TextInput())
    assigned_type = forms.CharField(required=True)
    assigned_to_user = forms.IntegerField(required=False)
    assigned_to_group = forms.IntegerField(required=False)
    start_date = forms.DateTimeField(required=True)
    due_date = forms.DateTimeField(required=True)
    priority = forms.CharField(required=True)
    status = forms.CharField(required=False)
    user_department = forms.IntegerField(required=False)
    document_file = forms.IntegerField(required=False)
    attached_resources = forms.FileField(required=False)
    comment = forms.CharField(required=False)

    class Meta:
        model = Task
        fields = ('task_title', 'task_description', 'assigned_type', 'assigned_to_user', 'assigned_to_group',
                  'start_date', 'due_date', 'priority', 'status', 'user_department', 'document_file',
                  'attached_resources', 'comment')

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        assigned_type = cleaned_data['assigned_type']
        if assigned_type == '1':
            if 'assigned_to_user' not in cleaned_data or cleaned_data['assigned_to_user'] == '' or cleaned_data['assigned_to_user'] is None:
                raise forms.ValidationError("Please Provide User id for assigning")
            else:
                cleaned_data['assigned_to_group'] = None
                cleaned_data['user_department'] = None
        if assigned_type == '2':
            if 'assigned_to_group' not in cleaned_data or cleaned_data['assigned_to_group'] == '' or cleaned_data['assigned_to_group'] is None:
                raise forms.ValidationError("Please Provide Group id for assigning")
            else:
                cleaned_data['assigned_to_user'] = None
                cleaned_data['user_department'] = None
        if assigned_type == '3':
            if 'user_department' not in cleaned_data or cleaned_data['user_department'] == '' or cleaned_data['user_department'] is None:
                raise forms.ValidationError("Please Provide User Department id for assigning")
            else:
                cleaned_data['assigned_to_user'] = None
                cleaned_data['assigned_to_group'] = None
        return cleaned_data


class TaskCommentForm(forms.Form):
    comment = forms.CharField(required=True)
    task = forms.CharField(required=True)

    class Meta:
        model = TaskComment
        fields = ('comment', 'task')

    def clean(self):
        cleaned_data = super(TaskCommentForm, self).clean()
        return cleaned_data


class TaskFileManagementForm(forms.Form):
    attached_resources = forms.FileField(required=True)
    task = forms.CharField(required=True)

    class Meta:
        model = TaskFileManagement
        fields = ('attached_resources', 'task')

    def clean(self):
        cleaned_data = super(TaskFileManagementForm, self).clean()
        if TaskFileManagement.objects.filter(task__id=cleaned_data['task']).exists():
            task_file_version = TaskFileManagement.objects.filter(task__id=cleaned_data['task']).last()
            cleaned_data['file_version'] = task_file_version.file_version + 1
            cleaned_data['is_same_file'] = task_file_version.id
        return cleaned_data


class ReassignTaskForm(forms.Form):
    assigned_type = forms.CharField(required=True)
    assigned_to_user = forms.IntegerField(required=False)
    assigned_to_group = forms.IntegerField(required=False)
    user_department = forms.IntegerField(required=False)
    
    class Meta:
        model = Task
        fields = ('assigned_type', 'assigned_to_user', 'assigned_to_group','user_department')

    def clean(self):
        cleaned_data = super(ReassignTaskForm, self).clean()
        assigned_type = cleaned_data['assigned_type']
        if assigned_type == '1':
            if 'assigned_to_user' not in cleaned_data or cleaned_data['assigned_to_user'] == '' or cleaned_data['assigned_to_user'] is None:
                raise forms.ValidationError("Please Provide User id for assigning")
            else:
                cleaned_data['assigned_to_group'] = None
                cleaned_data['user_department'] = None
        if assigned_type == '2':
            if 'assigned_to_group' not in cleaned_data or cleaned_data['assigned_to_group'] == '' or cleaned_data['assigned_to_group'] is None:
                raise forms.ValidationError("Please Provide Group id for assigning")
            else:
                cleaned_data['assigned_to_user'] = None
                cleaned_data['user_department'] = None
        if assigned_type == '3':
            if 'user_department' not in cleaned_data or cleaned_data['user_department'] == '' or cleaned_data['user_department'] is None:
                raise forms.ValidationError("Please Provide User Department id for assigning")
            else:
                cleaned_data['assigned_to_user'] = None
                cleaned_data['assigned_to_group'] = None
        return cleaned_data
