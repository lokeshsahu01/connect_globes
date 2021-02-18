from django import forms
from .models import *
from categories.models import *
from location.forms import *
from admin_users.forms import *
from ckeditor.widgets import CKEditorWidget


class CategoriesChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.category_name}'


class ProductForm(forms.ModelForm):
    product_code = forms.CharField(required=True)
    product_name = forms.CharField(required=True)
    product_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 8, 'cols': 100}))
    category = CategoriesChoiceField(queryset=Categories.objects.all(), required=True)
    product_gallery_image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    product_gallery_video = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    product_specification = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 8, 'cols': 100}))
    certificate_by = forms.CharField(required=False)
    certificate_file = forms.FileField(required=False)
    price = forms.FloatField(required=True, initial=0)
    selling_price = forms.FloatField(required=True, initial=0)
    slug = forms.CharField(required=True)
    meta_title = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 8, 'cols': 100}))
    meta_keyword = forms.CharField(required=False)
    status = forms.BooleanField(initial=True)

    class Meta:
        model = Product
        fields = ('product_code', 'product_name', 'slug', 'product_description', 'category', 'product_gallery_image', 'product_gallery_video', 'product_specification',
                  'certificate_by', 'certificate_file', 'price', 'selling_price', 'meta_title', 'meta_description', 'meta_keyword', 'status', 'is_approved')

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        if 'selling_price' in cleaned_data and cleaned_data['selling_price'] != 0:
            if cleaned_data['price'] < cleaned_data['selling_price']:
                raise forms.ValidationError("Selling price cannot be greater then price")
            cleaned_data['price_off'] = round(100 - (cleaned_data['selling_price'] * 100) / cleaned_data['price'])
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['product_name'].lower().replace(' ', '-')
        if Product.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        return cleaned_data


class ProductsChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.product_name}'


class ProductSizeForm(forms.ModelForm):
    product = ProductsChoiceField(queryset=Product.objects.all())
    size = forms.CharField(required=True)
    size_image = forms.FileField(required=False)
    alt = forms.CharField(required=False)
    is_feature = forms.BooleanField(required=False, initial=False)
    price = forms.IntegerField(required=False, initial=0)

    class Meta:
        model = ProductSize
        fields = ('product', 'size', 'size_image', 'alt', 'is_feature', 'price')

    def clean(self):
        cleaned_data = super(ProductSizeForm, self).clean()
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'size_image' in cleaned_data and cleaned_data['size_image']:
                cleaned_data['alt'] = cleaned_data['size_image'].name

        return cleaned_data


class BrandForm(forms.ModelForm):
    brand_name = forms.CharField(required=True)
    brand_image = forms.FileField(required=False)
    is_feature = forms.BooleanField(required=False, initial=False)
    is_approved = forms.BooleanField(required=False, initial=False)
    alt = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    meta_description = forms.CharField(required=False, widget=CKEditorWidget())
    meta_keyword = forms.CharField(required=False)
    meta_title = forms.CharField(required=False)

    class Meta:
        model = Brand
        fields = ('brand_name', 'brand_image', 'is_feature', 'is_approved', 'alt', 'slug', 'meta_title', 'meta_description', 'meta_keyword')

    def clean(self):
        cleaned_data = super(BrandForm, self).clean()
        if 'alt' not in cleaned_data or not cleaned_data['alt']:
            if 'brand_image' in cleaned_data and cleaned_data['brand_image'] and cleaned_data['brand_image'].name:
                cleaned_data['alt'] = cleaned_data['brand_image'].name
        if 'slug' not in cleaned_data or not cleaned_data['slug']:
            cleaned_data['slug'] = cleaned_data['brand_name'].lower().replace(' ', '-')
        if Brand.objects.filter(slug=cleaned_data['slug']).exists():
            raise forms.ValidationError('Slug Already exists !!!')
        return cleaned_data


class ShippingAddressForm(forms.ModelForm):
    full_name = forms.CharField(required=True)
    mobile_number = forms.CharField(required=True)
    country = CountryChoiceField(queryset=Country.objects.all())
    state = StateChoiceField(queryset=State.objects.all())
    city = CityChoiceField(queryset=City.objects.all())
    pin_code = forms.CharField(required=True)
    address = forms.CharField(required=True, widget=forms.Textarea)
    landmark = forms.CharField(required=False)
    is_default = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = ShippingAddress
        fields = ('full_name', 'mobile_number', 'country', 'state', 'city', 'pin_code', 'address', 'landmark', 'is_default')

    def clean(self):
        cleaned_data = super(ShippingAddressForm, self).clean()
        if cleaned_data['pin_code'].isdigit():
            if not Pincode.objects.filter(pincode=cleaned_data['pin_code']).exists():
                raise forms.ValidationError("Currently not available in this area.")
            cleaned_data['pincode'] = Pincode.objects.get(pincode=cleaned_data['pin_code'])
            cleaned_data.pop('pin_code')
        else:
            raise forms.ValidationError("Pin Code is not valid")
        return cleaned_data


class ProductInventoryForm(forms.ModelForm):
    product = ProductsChoiceField(queryset=Product.objects.all())
    stock_keeping_unit = forms.CharField(required=True)
    stock_quantity = forms.IntegerField(required=True)
    stock_status = forms.ChoiceField(required=False, choices=(('In stock', 'In stock'), ('Out of stock', 'Out of stock'), ('On backorder', 'On backorder')))
    allow_backorders = forms.ChoiceField(required=False, choices=(('Do not allow', 'Do not allow'), ('Allow, but notify customer', 'Allow, but notify customer'), ('Allow', 'Allow')))
    low_stock_threshold = forms.IntegerField(required=False)
    sold_individually = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = ProductInventory
        fields = ('product', 'stock_keeping_unit', 'stock_quantity', 'stock_status', 'allow_backorders', 'low_stock_threshold', 'sold_individually')

    def clean(self):
        cleaned_data = super(ProductInventoryForm, self).clean()
        return cleaned_data


class ProductShippingForm(forms.ModelForm):
    product = ProductsChoiceField(queryset=Product.objects.all())
    weight = forms.IntegerField(required=True)
    length = forms.IntegerField(required=True)
    width = forms.IntegerField(required=True)
    height = forms.IntegerField(required=True)

    class Meta:
        model = ProductInventory
        fields = ('product', 'weight', 'length', 'width', 'height')

    def clean(self):
        cleaned_data = super(ProductShippingForm, self).clean()
        return cleaned_data


class ProductColorForm(forms.ModelForm):
    product = ProductsChoiceField(queryset=Product.objects.all())
    color_code = forms.CharField(required=True)

    class Meta:
        model = ProductColor
        fields = ('product', 'color_code')

    def clean(self):
        cleaned_data = super(ProductColorForm, self).clean()
        return cleaned_data
