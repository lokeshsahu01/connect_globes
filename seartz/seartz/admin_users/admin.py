from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages
import os
import sys

from django.contrib.admin.sites import AdminSite
from django.conf.urls import url

from .views import HomeView


class DashboardSite(AdminSite):
    def get_urls(self):
        urls = super(DashboardSite , self).get_urls()
        custom_urls = [
            url(r'^$', self.admin_view(HomeView.as_view()), name='index'),
        ]

        del urls[0]
        return custom_urls + urls


class AdminUsersAdminView(admin.ModelAdmin):
    def get_departments(self, obj):
        if obj.user_department is not None:
            return UserDepartment.objects.get(id=obj.user_department).department

    def get_roles(self, obj):
        return UserRole.objects.get(id=obj.user_role).role

    list_display = ['mobile', 'get_departments', 'get_roles', 'date_joined']
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
