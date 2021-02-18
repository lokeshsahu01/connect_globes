from django.contrib import admin
from .forms import *
from django.contrib import messages
import sys


class ContactUsFormModelAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def username(self, obj):
        if obj.user:
            return obj.user.username

    list_display = ['id',  'username', 'first_name', 'last_name', 'contact_number', 'query_type', 'created_at']
    

class ContactUsContentModelAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id',  'username', 'title', 'slug', 'created_at']
    form = ContactUsContentForm
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ContactUsContentModelAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Contact Us Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                ContactUsContent(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    contact_us_content_obj = ContactUsContent.objects.filter(id=obj.id)
                    contact_us_content_obj.banner_image = form.cleaned_data['banner_image']
                    contact_us_content_obj.save()
                    form.cleaned_data.pop('banner_image')
                form.cleaned_data['updated_at'] = datetime.now()
                ContactUsContent.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Contact Us Page")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ContactUsIconsAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    def contact_us(self, obj):
        return obj.contact_us_content.title

    list_display = ['id',  'username', 'contact_us', 'title', 'icon_class', 'created_at']
    form = ContactUsIconsForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                ContactUsIcons(**form.cleaned_data).save()
            else:
                form.cleaned_data['updated_at'] = datetime.now()
                ContactUsIcons.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Contact Us Icon")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class TermsAndConditionsAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = TermsAndConditionsForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(TermsAndConditionsAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Contact Us Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                TermsAndConditions(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    contact_us_content_obj = TermsAndConditions.objects.filter(id=obj.id)
                    contact_us_content_obj.banner_image = form.cleaned_data['banner_image']
                    contact_us_content_obj.save()
                    form.cleaned_data.pop('banner_image')
                form.cleaned_data['updated_at'] = datetime.now()
                TermsAndConditions.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Terms And Conditions")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class PrivacyAndPolicyAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = PrivacyAndPolicyForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(PrivacyAndPolicyAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Contact Us Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                PrivacyAndPolicy(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    contact_us_content_obj = PrivacyAndPolicy.objects.filter(id=obj.id)
                    contact_us_content_obj.banner_image = form.cleaned_data['banner_image']
                    contact_us_content_obj.save()
                    form.cleaned_data.pop('banner_image')
                form.cleaned_data['updated_at'] = datetime.now()
                PrivacyAndPolicy.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Privacy And Policy")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class AboutUsAdminView(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = AboutUsForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(AboutUsAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Contact Us Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                AboutUs(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    contact_us_content_obj = AboutUs.objects.filter(id=obj.id)
                    contact_us_content_obj.banner_image = form.cleaned_data['banner_image']
                    contact_us_content_obj.save()
                    form.cleaned_data.pop('banner_image')
                form.cleaned_data['updated_at'] = datetime.now()
                AboutUs.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class FAndQAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'page', 'question', 'slug', 'created_at']
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


admin.site.register(ContactUsFormModel, ContactUsFormModelAdminView)
admin.site.register(ContactUsContent, ContactUsContentModelAdminView)
admin.site.register(ContactUsIcons, ContactUsIconsAdminView)
admin.site.register(TermsAndConditions, TermsAndConditionsAdminView)
admin.site.register(PrivacyAndPolicy, PrivacyAndPolicyAdminView)
admin.site.register(AboutUs, AboutUsAdminView)
admin.site.register(FAndQ, FAndQAdminView)
