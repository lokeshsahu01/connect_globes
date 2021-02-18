from django import forms
from .models import *


class CreateBlogForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.TextInput())
    status = forms.CharField(required=True)

    class Meta:
        model = Blog
        fields = ('title', 'content', 'status')

    def clean(self):
        cleaned_data = super(CreateBlogForm, self).clean()
        title = ''.join(i for i in cleaned_data['title'] if i.isalnum() or i == ' ')
        if '  ' in title:
            title = title.replace('  ', ' ')
        cleaned_data['slug'] = title.replace(' ', '-')
        return cleaned_data


class CreateBlogCommentForm(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.TextInput())
    sub_comment = forms.CharField(required=False)
    is_approved = forms.BooleanField(required=False)
    reject_reason = forms.CharField(required=False)

    class Meta:
        model = BlogComment
        fields = ('comment', 'sub_comment', 'is_approved', 'reject_reason')

    def clean(self):
        cleaned_data = super(CreateBlogCommentForm, self).clean()
        if 'sub_comment' in cleaned_data and cleaned_data['sub_comment'] != '' and cleaned_data['sub_comment'] is not None:
            if not BlogComment.objects.filter(id=cleaned_data['sub_comment']).exists():
                raise forms.ValidationError("Comment Not Exists !!!")
        else:
            del cleaned_data['sub_comment']
        return cleaned_data
