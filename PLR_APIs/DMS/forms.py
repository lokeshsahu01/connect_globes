from django import forms
from .models import *


class AllFoldersForm(forms.Form):
    parent_id = forms.CharField(required=False)
    folder_name = forms.CharField(required=True)
    account_id = forms.CharField(required=True)

    class Meta:
        model = AllFolders
        fields = ('parent_id', 'folder_name', 'account_id')

    def clean(self):
        cleaned_data = super(AllFoldersForm, self).clean()
        if 'parent_id' in cleaned_data and cleaned_data['parent_id'] != '' and cleaned_data['parent_id'] is not None:
            if not AllFolders.objects.filter(id=cleaned_data['parent_id'], user=CompanyUser.objects.get(account_id=cleaned_data['account_id'])).exists():
                raise forms.ValidationError("Folder Parent  Id Not Exists !!!")
        return cleaned_data


class CreateDMSForm(forms.Form):
    folder_id = forms.CharField(required=True)
    selected_user = forms.CharField(required=False)
    user_department = forms.CharField(required=False)
    file_content = forms.CharField(required=False)
    file_description = forms.CharField(required=False)
    status = forms.CharField(required=False)
    assigned_type = forms.CharField(required=True)
    file_tag = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = ScanFile
        fields = ('folder_id', 'selected_user', 'user_department', 'file_description', 'status', 'assigned_type',
                  'file_content', 'file_tag')

    def clean(self):
        cleaned_data = super(CreateDMSForm, self).clean()
        if not AllFolders.objects.filter(id=cleaned_data['folder_id']).exists():
            raise forms.ValidationError("Folder Not Exists !!!")
        if cleaned_data['assigned_type'] == '2' and 'user_department' in cleaned_data and cleaned_data['user_department'] is not None and cleaned_data['user_department'] != '':
            if not UserDepartment.objects.filter(id=cleaned_data['user_department']):
                raise forms.ValidationError("User Department Not Exists !!!")
        if cleaned_data['assigned_type'] == '1' and 'selected_user' in cleaned_data and cleaned_data['selected_user'] is not None and cleaned_data['selected_user'] != '':
            selected_user = eval(cleaned_data['selected_user'])
            for i in selected_user:
                if not CompanyUser.objects.filter(id=i).exists():
                    raise forms.ValidationError(f"User ID {i} Not Exists !!!")
        return cleaned_data


class DMSForm(forms.Form):
    selected_user = forms.CharField(required=False)
    user_department = forms.CharField(required=False)
    file_content = forms.CharField(required=False)
    file_description = forms.CharField(required=False)
    status = forms.CharField(required=False)
    assigned_type = forms.CharField(required=True)
    file_tag = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = ScanFile
        fields = ('selected_user', 'user_department', 'file_description', 'status', 'assigned_type',
                  'file_content', 'file_tag')

    def clean(self):
        cleaned_data = super(DMSForm, self).clean()
        return cleaned_data
