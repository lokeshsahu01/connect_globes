from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class BlogForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=CKEditorWidget())
    footer_content = forms.CharField(required=False, widget=CKEditorWidget())
    blog_banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    is_popular = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)
    slug = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget(), )
    meta_keyword = forms.CharField(required=False)

    class Meta:
        model = Blog
        fields = ('title', 'description', 'footer_content', 'blog_banner_image', 'alt', 'is_popular', 'is_active', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(BlogForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        if Blog.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'blog_banner_image' in cleaned_data and cleaned_data['blog_banner_image']:
                cleaned_data['alt'] = cleaned_data['blog_banner_image'].name
        return cleaned_data
