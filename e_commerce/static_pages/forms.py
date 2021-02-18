from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class ContactUsContentChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.title}'


class ContactUsContentForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = ContactUsContent
        fields = ('title', 'content', 'banner_image', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(ContactUsContentForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        if ContactUsContent.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class ContactUsIconsForm(forms.ModelForm):
    contact_us_content = ContactUsContentChoiceField(queryset=ContactUsContent.objects.all())
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    icon_class = forms.CharField(required=True)

    class Meta:
        model = ContactUsIcons
        fields = ('contact_us_content', 'title', 'content', 'icon_class')

    def clean(self):
        cleaned_data = super(ContactUsIconsForm, self).clean()
        return cleaned_data


class TermsAndConditionsForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = TermsAndConditions
        fields = ('title', 'content', 'banner_image', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(TermsAndConditionsForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        if TermsAndConditions.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class AboutUsForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = AboutUs
        fields = ('title', 'content', 'banner_image', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(AboutUsForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        print(AboutUs.objects.filter(slug=cleaned_data['slug']).exists())
        if AboutUs.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class PrivacyAndPolicyForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    banner_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = PrivacyAndPolicy
        fields = ('title', 'content', 'banner_image', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(PrivacyAndPolicyForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['title'].lower().replace(' ', '-')
        if PrivacyAndPolicy.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class FAndQForm(forms.ModelForm):
    page = forms.ChoiceField(required=True, choices=(('Contact Us', 'Contact Us'), ('Terms And Conditions', 'Terms And Conditions'), ('Privacy And Policy', 'Privacy And Policy'),
                                                     ('About Us', 'About Us')))
    question = forms.CharField(required=True)
    answer = forms.CharField(required=True, widget=CKEditorWidget())
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = FAndQ
        fields = ('page', 'question', 'answer', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(FAndQForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['question'].lower().replace(' ', '-')
        if FAndQ.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        return cleaned_data
