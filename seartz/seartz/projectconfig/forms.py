from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class HomeSliderForm(forms.ModelForm):
    slider_image = forms.FileField(required=True)
    description = forms.CharField(required=True, widget=CKEditorWidget())

    class Meta:
        model = HomeSlider
        fields = ('slider_image', 'description')

    def clean(self):
        cleaned_data = super(HomeSliderForm, self).clean()
        return cleaned_data


class GalleryCategoryForm(forms.ModelForm):
    category_name = forms.CharField(required=True)
    status = forms.BooleanField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea)
    meta_keyword = forms.CharField(required=False)

    class Meta:
        model = GalleryCategory
        fields = ('category_name', 'status', 'slug', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(GalleryCategoryForm, self).clean()
        slug = cleaned_data['category_name'].lower()
        if " " in slug:
            slug = slug.replace(' ', '-')
        cleaned_data['slug'] = slug
        return cleaned_data


class GalleryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=GalleryCategory.objects.all())
    image = forms.FileField(required=True)
    slug = forms.CharField(required=False)
    status = forms.BooleanField(required=False)
    alt = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea)
    meta_keyword = forms.CharField(required=False)

    class Meta:
        model = Gallery
        fields = ('category', 'image', 'slug', 'status', 'alt', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(GalleryForm, self).clean()
        if 'image' in cleaned_data and cleaned_data['image'] and cleaned_data['image'] != '':
            cleaned_data['image_name'] = cleaned_data['image'].name
            cleaned_data['image_size'] = cleaned_data['image'].size
            cleaned_data['alt'] = cleaned_data['image'].name
        if 'category' in cleaned_data:
            slug = cleaned_data['category'].category_name.lower()
            if " " in slug:
                slug = slug.replace(' ', '-')
            cleaned_data['slug'] = slug
            cleaned_data['category_id'] = cleaned_data['category'].id
            cleaned_data.pop('category')
        return cleaned_data


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
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class ContactUsIconsForm(forms.ModelForm):
    contact_us_content_id = ContactUsContentChoiceField(queryset=ContactUsContent.objects.all())
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=CKEditorWidget())
    icon_class = forms.CharField(required=True)

    class Meta:
        model = ContactUsContent
        fields = ('contact_us_content_id', 'title', 'content', 'icon_class')

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
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['alt'] = cleaned_data['banner_image'].name
        return cleaned_data


class ContactUsFormModelForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    contact_number = forms.CharField(required=True)
    email = forms.CharField(required=True)
    message = forms.CharField(required=True)
    query_type = forms.CharField(required=True)

    class Meta:
        model = ContactUsFormModel
        fields = ('first_name', 'last_name', 'contact_number', 'email', 'message', 'query_type')

    def clean(self):
        cleaned_data = super(ContactUsFormModelForm, self).clean()
        return cleaned_data


class TestimonialForm(forms.ModelForm):
    name = forms.CharField(required=True)
    banner_image = forms.FileField(required=False)
    banner_image_alt = forms.CharField(required=False)
    profile_image = forms.FileField(required=False)
    profile_image_alt = forms.CharField(required=False)
    description = forms.CharField(required=True, widget=CKEditorWidget())
    designation = forms.CharField(required=False)
    duration = forms.CharField(required=False)
    rating = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'Stars'}))
    social_link = forms.URLField(required=False)

    class Meta:
        model = ContactUsFormModel
        fields = ('name', 'banner_image', 'banner_image_alt', 'profile_image', 'profile_image_alt', 'description', 'designation', 'duration', 'rating', 'social_link')

    def clean(self):
        cleaned_data = super(TestimonialForm, self).clean()
        if 'banner_image_alt' in cleaned_data or cleaned_data['banner_image_alt']:
            if 'banner_image' in cleaned_data and cleaned_data['banner_image'] and cleaned_data['banner_image'].name:
                cleaned_data['banner_image_alt'] = cleaned_data['banner_image'].name
        if 'profile_image_alt' in cleaned_data or cleaned_data['profile_image_alt']:
            if 'profile_image' in cleaned_data and cleaned_data['profile_image'] and cleaned_data['profile_image'].name:
                cleaned_data['profile_image_alt'] = cleaned_data['profile_image'].name
        if 'rating' in cleaned_data:
            if cleaned_data['rating'] > 5 or cleaned_data['rating'] <= 0:
                raise forms.ValidationError('Rating Must 1 to 5')
        return cleaned_data
