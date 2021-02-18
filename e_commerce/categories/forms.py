from django import forms
from .models import *
import sys, os


class CategoriesChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.category_name}'


class CategoriesForm(forms.ModelForm):
    category_name = forms.CharField(required=True)
    status = forms.BooleanField(required=True, initial=True)
    category_image = forms.FileField(required=False)
    parent = CategoriesChoiceField(queryset=Categories.objects.all(), required=False)
    alt = forms.CharField(required=False)
    category_description = forms.CharField(required=False, widget=forms.Textarea())
    slug = forms.CharField(required=False, )
    meta_title = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea())
    meta_keyword = forms.CharField(required=False, )

    class Meta:
        model = Categories
        fields = ('category_name', 'status', 'category_image', 'alt', 'parent', 'category_description', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        try:
            cleaned_data = super(CategoriesForm, self).clean()
            cleaned_data['category_name'] = cleaned_data['category_name'].capitalize()
            if 'slug' not in cleaned_data or not cleaned_data['slug']:
                cleaned_data['slug'] = cleaned_data['category_name'].lower().replace(' ', '-')
            if Categories.objects.filter(slug=cleaned_data['slug']).exists():
                raise forms.ValidationError('Slug Already exists !!!')
            if 'alt' not in cleaned_data or not cleaned_data['alt']:
                if 'category_image' in cleaned_data and cleaned_data['category_image'] and cleaned_data['category_image'] != '':
                    cleaned_data['alt'] = cleaned_data['category_image'].name
            return cleaned_data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise forms.ValidationError(f"{e}, {f_name}, {exc_tb.tb_lineno}")
