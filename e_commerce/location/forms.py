from django import forms
from .models import *


class CountryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.country_name}'


class StateChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.state_name}'


class CityChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.city_name}'


class StateForm(forms.ModelForm):
    country = CountryChoiceField(queryset=Country.objects.all(), required=True)
    state_name = forms.CharField(required=True)
    state_image = forms.FileField(required=False)
    alt = forms.CharField(required=False, widget=forms.Textarea)
    is_popular = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)
    slug = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea)
    meta_keyword = forms.CharField(required=False)

    class Meta:
        model = State
        fields = ('country', 'state_name', 'state_image', 'alt', 'is_popular', 'is_active', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(StateForm, self).clean()
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'state_image' in cleaned_data and cleaned_data['state_image']:
                cleaned_data['alt'] = cleaned_data['state_image'].name
        if 'slug' not in cleaned_data or cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['state_name'].lower().replace(' ', '-')
        if State.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        return cleaned_data


class CityForm(forms.ModelForm):
    state = StateChoiceField(queryset=State.objects.all(), required=True)
    city_name = forms.CharField(required=True)
    city_image = forms.FileField(required=False)
    alt = forms.CharField(required=False, widget=forms.Textarea)
    is_popular = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)
    slug = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea)
    meta_keyword = forms.CharField(required=False)

    class Meta:
        model = City
        fields = ('state', 'city_name', 'city_image', 'alt', 'is_popular', 'is_active', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(CityForm, self).clean()
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'city_image' in cleaned_data and cleaned_data['city_image']:
                cleaned_data['alt'] = cleaned_data['city_image'].name
        if 'slug' not in cleaned_data or cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['city_name'].lower().replace(' ', '-')
        if City.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        return cleaned_data


class PincodeForm(forms.ModelForm):
    state = StateChoiceField(queryset=State.objects.all(), required=True)
    city = CityChoiceField(queryset=City.objects.all(), required=True)
    pincode = forms.CharField(required=True)
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = Pincode
        fields = ('state', 'city', 'pincode', 'is_active')

    def clean(self):
        cleaned_data = super(PincodeForm, self).clean()
        return cleaned_data
