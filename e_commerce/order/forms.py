from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class CouponCodeForm(forms.ModelForm):
    coupon_code = forms.CharField(required=True)
    coupon_discount_max_amount = forms.FloatField(required=True)
    coupon_discount_percentage = forms.FloatField(required=True)
    coupon_image = forms.FileField(required=False)
    alt = forms.CharField(required=False, widget=CKEditorWidget())
    is_valid = forms.BooleanField(required=False, initial=True)
    is_feature = forms.BooleanField(required=False, initial=True)
    coupon_description = forms.CharField(required=False, widget=CKEditorWidget())
    valid_for = forms.ChoiceField(required=False, choices=[('All Order', 'All Order'), ('First Order', 'First Order')])
    min_valid_amount = forms.FloatField(required=True)
    max_valid_amount = forms.FloatField(required=True)
    term_and_condition = forms.CharField(required=False, widget=CKEditorWidget())
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = CouponCode
        fields = ('coupon_code', 'coupon_discount_max_amount', 'coupon_discount_percentage', 'coupon_image', 'alt', 'is_valid', 'is_feature', 'coupon_description',
                  'valid_for', 'min_valid_amount', 'max_valid_amount', 'term_and_condition', 'slug', 'meta_description', 'meta_keyword', 'meta_keyword', 'meta_title')

    def clean(self):
        cleaned_data = super(CouponCodeForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['coupon_code'].lower().replace(' ', '-')
        if CouponCode.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'coupon_image' in cleaned_data and cleaned_data['coupon_image']:
                cleaned_data['alt'] = cleaned_data['coupon_image'].name
        return cleaned_data
