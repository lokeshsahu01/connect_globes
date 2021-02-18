from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class OurTeamForm(forms.ModelForm):
    name = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    profile_image = forms.FileField(required=False)
    designation = forms.CharField(required=False)
    rating = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'Stars'}))
    social_link = forms.URLField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = OurTeam
        fields = ('name', 'content', 'profile_image', 'designation', 'rating', 'social_link', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(OurTeamForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['name'].lower().replace(' ', '-')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        if 'rating' in cleaned_data:
            if cleaned_data['rating'] > 5 or cleaned_data['rating'] <= 0:
                raise forms.ValidationError('Rating Must 1 to 5')
        return cleaned_data


class VisionForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = OurTeam
        fields = ('title', 'content', 'banner_image', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(VisionForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class MissionForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = OurTeam
        fields = ('title', 'content', 'banner_image', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(MissionForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class FAndQForm(forms.ModelForm):
    question = forms.CharField(required=True)
    answer = forms.CharField(required=True, widget=CKEditorWidget())
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = OurTeam
        fields = ('question', 'answer', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(FAndQForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['question'].lower().replace(' ', '-')

        return cleaned_data
