from CompanyUser.models import *
import os
from django.conf import settings


class AllFolders(models.Model):
    parent_id = models.ForeignKey('AllFolders', on_delete=models.CASCADE, blank=True, null=True, related_name='folders')
    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ScanFile(models.Model):
    def folder_path(self, filename):
        folder_path = upper_tree_folder(self.folder_id) + self.folder_id.folder_name

        if self.user.is_company:
            user_path = os.path.join(f"plr/{str(self.user.username)}/Documents{folder_path}")
        else:
            user_path = os.path.join(f"plr/{str(self.user.company_sub_user_id.username)}/{str(self.user.username)}/Documents{folder_path}")
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        return os.path.join(user_path, filename)

    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    folder_id = models.ForeignKey(AllFolders, on_delete=models.CASCADE, blank=True, null=True)
    assigned_type = models.CharField(max_length=10, choices=[('1', 'User'), ('2', 'department')], default='1')
    selected_user = models.CharField(max_length=255, default=None, blank=True, null=True)
    user_department = models.ForeignKey('CompanyUser.UserDepartment', on_delete=models.CASCADE,
                                        related_name='file_user_department', null=True, blank=True)
    upload_file = models.FileField(upload_to=folder_path, null=True, blank=True)
    file_size = models.CharField(max_length=255, default='0')
    file_version = models.CharField(max_length=255, default='0')
    file_description = models.TextField(max_length=5000, null=True, blank=True)
    file_content = models.TextField(max_length=5000, null=True, blank=True)
    upload_type = models.CharField(max_length=100)
    batch_no = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class FileTag(models.Model):
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    file_id = models.ForeignKey(ScanFile, on_delete=models.CASCADE)
    file_tag = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


def lower_tree_folder(parent_obj):
    def child_tree_folder(obj, folder_path):
        if AllFolders.objects.filter(parent_id=obj).exists():
            child_folder = AllFolders.objects.filter(parent_id=obj)
            for k in child_folder:
                folder_path.append(k)
                child_tree_folder(k, folder_path)
            return folder_path
    return child_tree_folder(parent_obj, [])


def upper_tree_folder(parent_obj):
    def parent_tree_folder(obj, folder_path):
        if obj.parent_id is not None:
            child_folder = AllFolders.objects.get(id=obj.parent_id.id)
            folder_path += f'/{child_folder.folder_name}'
            folder_path = parent_tree_folder(child_folder, folder_path)
            return folder_path
        else:
            return folder_path
    return parent_tree_folder(parent_obj, '') + '/'
