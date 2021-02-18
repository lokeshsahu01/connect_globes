from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .forms import *
from django.contrib import messages
import sys


class BlogAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def approved(self, obj):
        if obj.is_approved:
            html = f'''<a href="/api/v1/blog/approved/{obj.id}"><img src="/static/admin/img/icon-yes.svg" alt="False"></a>'''
        else:
            html = f'''<a href="/api/v1/blog/approved/{obj.id}"><img src="/static/admin/img/icon-no.svg" alt="True"></a>'''
        return format_html(html)

    list_display = ['title', 'user_id', 'content', 'status', 'slug', 'approved', 'approved_by', 'created_at']


class BlogCommentAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def approved(self, obj):
        if obj.is_approved:
            html = f'''<a href="/api/v1/blog/comment/approved/{obj.id}/"><img src="/static/admin/img/icon-yes.svg" alt="False"></a>'''
        else:
            html = f'''<a href="/api/v1/blog/comment/approved/{obj.id}/"><img src="/static/admin/img/icon-no.svg" alt="True"></a>'''
        return format_html(html)

    def blog(self, obj):
        return Blog.objects.get(id=obj.blog_id).title

    def username(self, obj):
        return User.objects.get(id=obj.user_id).username

    list_display = ['id', 'comment', 'blog', 'username', 'sub_comment', 'approved', 'approved_by', 'unapproved_by', 'reject_reason', 'created_at']
    form = CreateBlogCommentForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(BlogCommentAdminView, self).get_form(request, obj, **kwargs)
        form.base_fields['comment'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        form.base_fields['sub_comment'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        return form


admin.site.register(Blog, BlogAdminView)
admin.site.register(BlogComment, BlogCommentAdminView)
