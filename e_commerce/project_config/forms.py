from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget


class SocialMediaIconForm(forms.ModelForm):
    icon_name = forms.CharField(required=True)
    icon_url = forms.CharField(required=False)
    icon_class = forms.CharField(required=False)

    class Meta:
        model = SocialMediaIcon
        fields = ('icon_name', 'icon_url', 'icon_class')

    def clean(self):
        cleaned_data = super(SocialMediaIconForm, self).clean()
        return cleaned_data


class CopyrightForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=CKEditorWidget())

    class Meta:
        model = Copyright
        fields = ('content',)

    def clean(self):
        cleaned_data = super(CopyrightForm, self).clean()
        return cleaned_data
