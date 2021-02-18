from django import forms
from .models import *
from categories.hierarchical_category import *
import re


class ProductForm(forms.ModelForm):
    product_code = forms.CharField(required=True)
    product_name = forms.CharField(required=True)
    product_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 8, 'cols': 100}))
    product_category = forms.ChoiceField(choices=lambda: get_categories(False), required=True)
    product_home_image = forms.FileField(required=False)
    product_gallery_image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    product_specification = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 8, 'cols': 100}))
    certificate_by = forms.CharField(required=False)
    certificate_file = forms.FileField(required=False)
    price = forms.FloatField(required=False, initial=0)
    selling_price = forms.FloatField(required=False, initial=0)
    available_stock = forms.IntegerField(required=False, initial=0)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 8, 'cols': 100}))
    meta_keyword = forms.CharField(required=False)
    status = forms.ChoiceField(choices=(('Published', 'Published'), ('Post', 'Post'), ('Draft', 'Draft')))

    class Meta:
        model = Product
        fields = ('product_code', 'product_name', 'slug', 'product_description', 'product_category', 'product_home_image', 'product_gallery_image', 'product_specification',
                  'certificate_by', 'certificate_file', 'price', 'selling_price', 'available_stock', 'meta_description', 'meta_keyword', 'status', 'is_approved')

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = re.sub("[()\[\]{}!#%^*$@&,./'\";:|\\\<>?]", "", cleaned_data['product_name'].lower().replace(' ', '-'))
            if cleaned_data['slug'][-1] == '-':
                cleaned_data['slug'] = cleaned_data['slug'][:-1]
        if 'price' in cleaned_data and cleaned_data['price'] and 'selling_price' in cleaned_data and cleaned_data['selling_price']:
            if cleaned_data['price'] < cleaned_data['selling_price']:
                raise forms.ValidationError("Selling price cannot be greater then price")
            cleaned_data['price_off'] = round(100 - (cleaned_data['selling_price'] * 100) / cleaned_data['price'])
        cleaned_data['category_id'] = Categories.objects.get(category_name=cleaned_data['product_category'].strip(' ')).id
        del cleaned_data['product_category']
        return cleaned_data


class ProductChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.product_name}'


class ProductGalleryImageFrom(forms.ModelForm):
    product_id = ProductChoiceField(queryset=Product.objects.all(), required=False)
    product_gallery_image = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = ('product_id', 'product_gallery_image')

    def clean(self):
        cleaned_data = super(ProductGalleryImageFrom, self).clean()
        cleaned_data['product_id'] = cleaned_data['product_id'].id
        return cleaned_data


class ProductSizeForm(forms.ModelForm):
    product_id = ProductChoiceField(queryset=Product.objects.all(), required=False)
    size = forms.CharField(required=True)
    size_image = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = ('product_id', 'size', 'size_image')

    def clean(self):
        cleaned_data = super(ProductSizeForm, self).clean()
        cleaned_data['product_id'] = cleaned_data['product_id'].id
        return cleaned_data


class ProductCanvasForm(forms.ModelForm):
    product_id = ProductChoiceField(queryset=Product.objects.all(), required=False)
    canvas = forms.CharField(required=True)
    canvas_image = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = ('product_id', 'canvas', 'canvas_image')

    def clean(self):
        cleaned_data = super(ProductCanvasForm, self).clean()
        cleaned_data['product_id'] = cleaned_data['product_id'].id
        return cleaned_data
