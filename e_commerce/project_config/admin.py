from django.contrib import admin
from .forms import *
from django.contrib import messages
import sys


class SocialMediaIconAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'username', 'icon_name', 'icon_class', 'icon_url', 'created_at']
    form = SocialMediaIconForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                SocialMediaIcon(**form.cleaned_data).save()
            else:
                form.cleaned_data['updated_at'] = datetime.now()
                SocialMediaIcon.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class NewsletterAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def username(self, obj):
        if obj.user:
            return obj.user.username

    list_display = ['id', 'username', 'email', 'created_at']


class CopyrightAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'username', 'content', 'created_at']
    form = CopyrightForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                Copyright(**form.cleaned_data).save()
            else:
                form.cleaned_data['updated_at'] = datetime.now()
                Copyright.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(SocialMediaIcon, SocialMediaIconAdminView)
admin.site.register(Newsletter, NewsletterAdminView)
admin.site.register(Copyright, CopyrightAdminView)
