from django import forms
from .models import *
import sys, os
from .hierarchical_category import *


class CategoriesForm(forms.ModelForm):
    category_name = forms.CharField(required=True)
    status = forms.ChoiceField(required=True, choices=[('Inactive', 'Inactive'), ('Active', 'Active')], initial="Active")
    category_image = forms.FileField(required=False)
    category = forms.ChoiceField(required=False)
    category_description = forms.CharField(required=False, widget=forms.Textarea())
    slug = forms.CharField(required=False, )
    meta_description = forms.CharField(required=False, widget=forms.Textarea())
    meta_keyword = forms.CharField(required=False, )

    class Meta:
        model = Categories
        fields = ('category_name', 'status', 'category_image', 'category', 'category_description', 'slug',
                  'meta_description', 'meta_keyword')

    def clean(self):
        try:
            cleaned_data = super(CategoriesForm, self).clean()
            if cleaned_data['category'] is not None and cleaned_data['category'] != '':
                cleaned_data['sub_category'] = Categories.objects.get(category_name=cleaned_data['category'].strip(' ')).id
            else:
                cleaned_data['sub_category'] = None
            del cleaned_data['category']
            cleaned_data['category_name'] = cleaned_data['category_name'].capitalize()
            slug = cleaned_data['category_name'].lower()
            if " " in slug:
                slug = '-'.join(i for i in slug.split(" "))
            cleaned_data['slug'] = slug
            return cleaned_data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise forms.ValidationError(f"{e}, {f_name}, {exc_tb.tb_lineno}")
