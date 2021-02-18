from django import forms
from .models import *


class CreateCartForm(forms.Form):
    product = forms.CharField(required=True)
    quantity = forms.IntegerField(required=True)

    class Meta:
        model = Cart
        fields = ('product', 'quantity')

    def clean(self):
        cleaned_data = super(CreateCartForm, self).clean()
        if not Product.objects.filter(id=cleaned_data['product']).exists():
            raise forms.ValidationError("Product not found")
        return cleaned_data


class CreateOrderAddressForm(forms.Form):
    full_name = forms.CharField(required=True)
    mobile_number = forms.IntegerField(required=True)
    pin_code = forms.IntegerField(required=True)
    address = forms.CharField(required=True, widget=forms.Textarea())
    landmark = forms.CharField(required=False)
    town_city = forms.CharField(required=True)
    State = forms.CharField(required=True)
    address_type = forms.CharField(required=True)
    is_default = forms.IntegerField(required=True)

    class Meta:
        model = Cart
        fields = ('full_name', 'mobile_number', 'pin_code', 'address', 'landmark', 'town_city', 'State', 'address_type', 'is_default')

    def clean(self):
        cleaned_data = super(CreateOrderAddressForm, self).clean()
        if cleaned_data['is_default']:
            cleaned_data['is_default'] = True
        else:
            cleaned_data['is_default'] = False
        return cleaned_data


class CreateOrderForm(forms.Form):
    order_address_id = forms.CharField(required=True)
    coupon_code = forms.CharField(required=False)
    payment_method = forms.CharField(required=True)
    razorpay_payment_id = forms.CharField(required=False)

    class Meta:
        model = Cart
        fields = ('order_address_id', 'coupon_code', 'payment_method', 'razorpay_payment_id')

    def clean(self):
        cleaned_data = super(CreateOrderForm, self).clean()
        if not OrderAddress.objects.filter(id=cleaned_data['order_address_id']).exists():
            raise forms.ValidationError("Address Is not Saved")
        if 'coupon_code' in cleaned_data and cleaned_data['coupon_code'] and not CouponCode.objects.filter(coupon_code=cleaned_data['coupon_code']).exists() and not CouponCode.objects.get(coupon_code=cleaned_data['coupon_code']).is_valid:
            raise forms.ValidationError("Coupon Code Is not Valid")

        return cleaned_data


class CouponCodeeForm(forms.ModelForm):
    class Meta:
        model = CouponCode
        fields = '__all__'
