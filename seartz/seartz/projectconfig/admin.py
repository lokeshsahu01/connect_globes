from django.contrib import admin
from .forms import *
from django.contrib import messages
from django.utils.html import format_html
import sys
from admin_users.models import *
from django.core.files.storage import FileSystemStorage


class HomeSliderAdminView(admin.ModelAdmin):
    def feature(self, obj):
        if obj.is_featured:
            html = f'''<a href="/api/v1/home/slider/feature/{obj.id}"><img src="/static/admin/img/icon-no.svg" alt="False"></a>'''
        else:
            html = f'''<a href="/api/v1/home/slider/feature/{obj.id}"><img src="/static/admin/img/icon-yes.svg" alt="True"></a>'''
        return format_html(html)

    list_display = ['id', 'user_id', 'slider_image', 'feature', 'featured_user_id', 'created_at']
    form = HomeSliderForm

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            form.cleaned_data['user_id'] = request.user.id
            HomeSlider(**form.cleaned_data).save()
        else:
            year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
            folder = f'media/HomeSlider/{year}/{month}/{date}'
            fs = FileSystemStorage(location=folder)
            filename = fs.save(form.cleaned_data['slider_image'].name, form.cleaned_data['slider_image'])
            home_slider_obj = HomeSlider.objects.filter(id=obj.id).update(slider_image=folder.replace('media/', '') + f"/{form.cleaned_data['slider_image'].name}",
                                                                          description=form.cleaned_data['description'],
                                                                          featured_user_id=request.user.id, updated_at=datetime.now())

        messages.info(request, "Successfully Apply Changes")


class GalleryCategoryAdminView(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'status', 'slug', 'created_at']
    form = GalleryCategoryForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(GalleryCategoryAdminView, self).get_form(request, obj, **kwargs)
        if obj is None:
            for key in ['status', 'slug', 'meta_description', 'meta_keyword']:
                del form.base_fields[key]
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                GalleryCategory(**form.cleaned_data).save()
                cat = GalleryCategory.objects.last()
                messages.info(request, f"Category {cat.category_name} {cat.slug} Successfully Created")
            else:
                GalleryCategory.objects.filter(id=obj.id).update(**form.cleaned_data)
                gallery_category_obj = GalleryCategory.objects.get(id=obj.id)
                messages.info(request, f"Category {gallery_category_obj.category_name} {gallery_category_obj.slug} Successfully Updated")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class GalleryAdminView(admin.ModelAdmin):
    def category(self, obj):
        return GalleryCategory.objects.get(id=obj.category_id).category_name

    list_display = ['id', 'user_id', 'category', 'image_name', 'image_size', 'image', 'alt', 'slug', 'status', 'created_at']
    form = GalleryForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(GalleryAdminView, self).get_form(request, obj, **kwargs)
        if obj is None:
            for key in ['slug', 'status', 'alt', 'meta_description', 'meta_keyword']:
                del form.base_fields[key]
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                Gallery(**form.cleaned_data).save()
                messages.info(request, f"Gallery Successfully Created")
            else:
                if 'image' not in form.cleaned_data or not form.cleaned_data['image'] or form.cleaned_data['image'] == '':
                    form.cleaned_data.pop('image')
                else:
                    year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
                    folder = f'media/Gallery/{year}/{month}/{date}'
                    fs = FileSystemStorage(location=folder)
                    filename = fs.save(form.cleaned_data['image'].name, form.cleaned_data['image'])
                    form.cleaned_data['image'] = folder.replace('media/', '') + f"/{form.cleaned_data['image'].name}"
                Gallery.objects.filter(id=obj.id).update(**form.cleaned_data)
                messages.info(request, f"Gallery Successfully Updated")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ContactUsFormModelAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'first_name', 'last_name', 'contact_number', 'query_type', 'created_at']


class ContactUsContentModelAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
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
                form.cleaned_data['user_id'] = request.user.id
                ContactUsContent(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    banner_image_fs = FileSystemStorage('media/ContactUs/')
                    banner_image_file = banner_image_fs.save(form.cleaned_data['banner_image'].name, form.cleaned_data['banner_image'])
                    form.cleaned_data['banner_image'] = 'ContactUs/' + banner_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                ContactUsContent.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Contact Us Page")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ContactUsIconsAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    def contact_us(self, obj):
        return ContactUsContent.objects.get(id=obj.contact_us_content).title

    list_display = ['id', 'username', 'contact_us', 'title', 'icon_class', 'created_at']
    form = ContactUsIconsForm

    def save_model(self, request, obj, form, change):
        try:
            if 'contact_us_content_id' in form.cleaned_data:
                form.cleaned_data['contact_us_content'] = form.cleaned_data['contact_us_content_id'].id
                form.cleaned_data.pop('contact_us_content_id')
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
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
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = ContactUsContentForm

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
                form.cleaned_data['user_id'] = request.user.id
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
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = ContactUsContentForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(PrivacyAndPolicyAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Privacy And Policy Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                PrivacyAndPolicy(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    banner_image_fs = FileSystemStorage('media/PrivacyAndPolicy/')
                    banner_image_file = banner_image_fs.save(form.cleaned_data['banner_image'].name, form.cleaned_data['banner_image'])
                    form.cleaned_data['banner_image'] = 'PrivacyAndPolicy/' + banner_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                PrivacyAndPolicy.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Privacy And Policy")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class AboutUsAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'username', 'title', 'slug', 'created_at']
    form = ContactUsContentForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(AboutUsAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="About Us Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                AboutUs(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    banner_image_fs = FileSystemStorage('media/AboutUs/')
                    banner_image_file = banner_image_fs.save(form.cleaned_data['banner_image'].name, form.cleaned_data['banner_image'])
                    form.cleaned_data['banner_image'] = 'AboutUs/' + banner_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                AboutUs.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on About Us")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class TestimonialAdminView(admin.ModelAdmin):

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    def feature(self, obj):
        if obj.is_featured:
            html = f'''<a href="/api/v1/home/testimonial/feature/{obj.id}"><img src="/static/admin/img/icon-yes.svg" alt="False"></a>'''
        else:
            html = f'''<a href="/api/v1/home/testimonial/feature/{obj.id}"><img src="/static/admin/img/icon-no.svg" alt="True"></a>'''
        return format_html(html)

    list_display = ['id', 'username', 'name', 'designation', 'description', 'rating', 'rating', 'social_link', 'feature']
    form = TestimonialForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(TestimonialAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.banner_image.name:
                filename = f'''<img src="{obj.banner_image.url}" alt="Testimonial Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['banner_image'].help_text = filename

            if obj.profile_image.name:
                filename = f'''<img src="{obj.profile_image.url}" alt="Testimonial Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['profile_image'].help_text = filename

        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user_id'] = request.user.id
                Testimonial(**form.cleaned_data).save()
            else:
                if 'banner_image' in form.cleaned_data and form.cleaned_data['banner_image']:
                    banner_image_fs = FileSystemStorage('media/Testimonial/')
                    banner_image_file = banner_image_fs.save(form.cleaned_data['banner_image'].name, form.cleaned_data['banner_image'])
                    form.cleaned_data['banner_image'] = 'Testimonial/' + banner_image_file
                if 'profile_image' in form.cleaned_data and form.cleaned_data['profile_image']:
                    profile_image_fs = FileSystemStorage('media/Testimonial/')
                    profile_image_file = profile_image_fs.save(form.cleaned_data['profile_image'].name, form.cleaned_data['profile_image'])
                    form.cleaned_data['profile_image'] = 'Testimonial/' + profile_image_file
                form.cleaned_data['updated_at'] = datetime.now()
                Testimonial.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Testimonial")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(HomeSlider, HomeSliderAdminView)
admin.site.register(Gallery, GalleryAdminView)
admin.site.register(GalleryCategory, GalleryCategoryAdminView)
admin.site.register(ContactUsFormModel, ContactUsFormModelAdminView)
admin.site.register(ContactUsContent, ContactUsContentModelAdminView)
admin.site.register(ContactUsIcons, ContactUsIconsAdminView)
admin.site.register(TermsAndConditions, TermsAndConditionsAdminView)
admin.site.register(PrivacyAndPolicy, PrivacyAndPolicyAdminView)
admin.site.register(AboutUs, AboutUsAdminView)
admin.site.register(Testimonial, TestimonialAdminView)
admin.site.enable_nav_sidebar = False
