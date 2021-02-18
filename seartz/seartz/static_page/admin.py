from django.contrib import admin
from .forms import *
from django.contrib import messages
from django.utils.html import format_html
import sys
from admin_users.models import *
from django.core.files.storage import FileSystemStorage


class OurTeamAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'name', 'slug', 'created_at']
    form = OurTeamForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(OurTeamAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.profile_image.name:
                filename = f'''<img src="{obj.profile_image.url}" alt="Our Team Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['profile_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                OurTeam(**form.cleaned_data).save()
            else:
                if 'profile_image' in form.cleaned_data and form.cleaned_data['profile_image']:
                    profile_image_fs = FileSystemStorage('media/OurTeam/')
                    profile_image_file = profile_image_fs.save(form.cleaned_data['profile_image'].name, form.cleaned_data['profile_image'])
                    form.cleaned_data['profile_image'] = 'OurTeam/' + profile_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                OurTeam.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class VisionAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = VisionForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(VisionAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Vision Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                Vision(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    banner_image_fs = FileSystemStorage('media/Vision/')
                    banner_image_file = banner_image_fs.save(form.cleaned_data['banner_image'].name, form.cleaned_data['banner_image'])
                    form.cleaned_data['banner_image'] = 'Vision/' + banner_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                Vision.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class MissionAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = MissionForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(MissionAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Mission Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                Mission(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    banner_image_fs = FileSystemStorage('media/Mission/')
                    banner_image_file = banner_image_fs.save(form.cleaned_data['banner_image'].name, form.cleaned_data['banner_image'])
                    form.cleaned_data['banner_image'] = 'Mission/' + banner_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                Mission.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class FAndQAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'question', 'slug', 'created_at']
    form = FAndQForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                FAndQ(**form.cleaned_data).save()
            else:
                form.cleaned_data['updated_at'] = datetime.now()
                FAndQ.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(OurTeam, OurTeamAdminView)
admin.site.register(Vision, VisionAdminView)
admin.site.register(Mission, MissionAdminView)
admin.site.register(FAndQ, FAndQAdminView)
