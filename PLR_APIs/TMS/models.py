from CompanyUser.models import *


class Group(models.Model):
    created_by = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, blank=True, null=True)
    selected_user_list = models.CharField(max_length=100, verbose_name='Selected User List')
    total_user = models.CharField(max_length=100, verbose_name='Total User')
    group_name = models.CharField(max_length=100, verbose_name='Group Name')
    group_desc = models.CharField(max_length=300, verbose_name='Group Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    user = models.ForeignKey('CompanyUser.CompanyUser', default=None, on_delete=models.CASCADE,
                             related_name='created_task_by')
    task_title = models.CharField(max_length=200, verbose_name='Task Title')
    task_description = models.CharField(max_length=1000, verbose_name='Task Description')
    assigned_type = models.CharField(max_length=10, choices=[('1', 'User'), ('2', 'Group'), ('3', 'department')])
    assigned_to_user = models.ForeignKey('CompanyUser.CompanyUser', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='assigned_to_user')
    assigned_to_group = models.ForeignKey('Group', default=None, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name='assigned_to_group')
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, default='Normal')
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('In Progress', 'In Progress'),
                                                      ('Done', 'Done')], default='Open')
    task_type = models.CharField(max_length=2, choices=[('1', 'General'), ('2', 'Document Task')], default='1')
    user_department = models.ForeignKey('CompanyUser.UserDepartment', on_delete=models.CASCADE, related_name='user_department',
                                        null=True, blank=True)
    document_file = models.ForeignKey('DMS.ScanFile', on_delete=models.CASCADE, related_name='document_file', null=True,
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TaskFileManagement(models.Model):
    def folder_path(self, filename):
        if self.user.is_company:
            upload_dir = os.path.join('plr/', str(self.user.username)+'/Task/')
            return os.path.join(upload_dir, filename)
        else:
            upload_dir = os.path.join('plr/', str(self.user.company_sub_user_id.username) + '/' +
                                      str(self.user.username) + '/'+'Task/')
            return os.path.join(upload_dir, filename)
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=250, null=True, blank=True)
    file_size = models.CharField(max_length=250, null=True, blank=True)
    is_same_file = models.ForeignKey('TaskFileManagement', on_delete=models.CASCADE, blank=True, null=True)
    file_version = models.IntegerField(default=1)
    attached_resources = models.FileField(upload_to=folder_path, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TaskActivityLogs(models.Model):
    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE)
    log_type = models.CharField(max_length=250)
    log_description = models.TextField(max_length=65500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TaskComment(models.Model):
    comment = models.CharField(max_length=500, verbose_name='Comment')
    user = models.ForeignKey(CompanyUser, default=None, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, default=None, on_delete=models.CASCADE, verbose_name='Task Primary Comment Id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
