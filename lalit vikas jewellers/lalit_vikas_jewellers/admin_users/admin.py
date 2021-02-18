from django.contrib import admin
from .models import *
from .forms import *


class AdminUsersAdminView(admin.ModelAdmin):
    def get_departments(self, obj):
        return obj.user_department.department

    def get_roles(self, obj):
        return obj.user_role.role

    list_display = ['username', 'get_departments', 'get_roles', 'date_joined']
    form = AdminUsersForm

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(AdminUsersAdminView, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest


class UserRoleAdminView(admin.ModelAdmin):
    list_display = ['role', 'created_at']


class UserDepartmentAdminView(admin.ModelAdmin):
    list_display = ['department', 'created_at']


admin.site.register(UserRole, UserRoleAdminView)
admin.site.register(UserDepartment, UserDepartmentAdminView)
admin.site.register(User, AdminUsersAdminView)
