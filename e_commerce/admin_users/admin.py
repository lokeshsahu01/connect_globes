from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages
import sys
from django.utils.html import format_html


class AdminUsersAdminView(admin.ModelAdmin):
    def get_departments(self, obj):
        if obj.user_department is not None:
            return obj.user_department.department

    def get_roles(self, obj):
        return obj.user_role.role

    list_display = ['account_id', 'username',  'get_departments', 'get_roles', 'mobile', 'first_name', 'last_name', 'is_mobile', 'is_email', 'is_active', 'date_joined']
    form = AdminUsersForm

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(AdminUsersAdminView, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormWithRequest

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                if form.cleaned_data['user_role'].is_create_user:
                    form.cleaned_data['is_superuser'] = True
                User(**form.cleaned_data).save()
            else:
                if form.cleaned_data['user_role'].is_create_user:
                    form.cleaned_data['is_superuser'] = True
                else:
                    form.cleaned_data['is_superuser'] = False
                User.objects.filter(id=obj.id).update(**form.cleaned_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class UserRoleAdminView(admin.ModelAdmin):
    list_display = ['role', 'created_at']


class UserDepartmentAdminView(admin.ModelAdmin):
    list_display = ['department', 'created_at']


admin.site.register(UserRole, UserRoleAdminView)
admin.site.register(UserDepartment, UserDepartmentAdminView)
admin.site.register(User, AdminUsersAdminView)
admin.site.enable_nav_sidebar = False
