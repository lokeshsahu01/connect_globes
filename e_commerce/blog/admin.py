from django.contrib import admin
from .forms import *
from django.utils.html import format_html
from django.contrib import messages
import sys


class BlogAdminView(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def popular(self, obj):
        return format_html(f'''<a href="/api/v1/blog/popular/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_popular else 'no'}.svg" alt="True"></a>''')

    def active(self, obj):
        return format_html(f'''<a href="/api/v1/blog/active/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_active else 'no'}.svg" alt="True"></a>''')

    list_display = ['id', 'username', 'title', 'popular', 'active', 'slug', 'created_at']
    form = BlogForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(BlogAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.blog_banner_image.name:
                filename = f'''<img src="{obj.blog_banner_image.url}" alt="Product Gallery Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['blog_banner_image'].help_text = filename
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                Blog(**form.cleaned_data).save()
            else:
                Blog.objects.filter(id=obj.id).update(**form.cleaned_data)
            messages.info(request, "Successfully Applied Changes on Product Color")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class BlogCommentAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def username(self, obj):
        return obj.user.username

    list_display = ['id',  'user', 'blog', 'comment', 'sub_comment', 'is_approved', 'approved_by', 'is_feature', 'created_at']


admin.site.register(Blog, BlogAdminView)
admin.site.register(BlogComment, BlogCommentAdminView)
