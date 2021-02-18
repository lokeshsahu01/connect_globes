from django.contrib import admin
from .models import *
from django.contrib import messages
from django.utils.html import format_html
from .forms import *


class CountryAdminView(admin.ModelAdmin):
    list_display = ['country_name', 'country_code', 'country_currency', 'country_phone_code', 'created_at']


class StateAdminView(admin.ModelAdmin):
    def country_name(self, obj):
        return obj.country.country_name

    def popular(self, obj):
        return format_html(f'''<a href="/api/v1/location/state/popular/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_popular else 'no'}.svg" alt="True"></a>''')

    def active(self, obj):
        return format_html(f'''<a href="/api/v1/location/state/active/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_active else 'no'}.svg" alt="True"></a>''')

    list_display = ['state_name', 'country_name', 'popular', 'active', 'slug', 'created_at']
    form = StateForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(StateAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.state_image.name:
                filename = f'''<img src="{obj.state_image.url}" alt="Product Gallery Image" width="50" height="50" style="padding:5px">'''
                form.base_fields['state_image'].help_text = filename
        return form


class CityAdminView(admin.ModelAdmin):
    def state_name(self, obj):
        return obj.state.state_name

    def popular(self, obj):
        return format_html(f'''<a href="/api/v1/location/city/popular/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_popular else 'no'}.svg" alt="True"></a>''')

    def active(self, obj):
        return format_html(f'''<a href="/api/v1/location/city/active/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_active else 'no'}.svg" alt="True"></a>''')

    list_display = ['city_name', 'state_name', 'popular', 'active', 'slug', 'created_at']
    form = CityForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(CityAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.city_image.name:
                filename = f'''<img src="{obj.city_image.url}" alt="Product Gallery Image" width="300" height="120" style="padding:5px">'''
                form.base_fields['city_image'].help_text = filename
        return form


class PincodeAdminView(admin.ModelAdmin):
    def state_name(self, obj):
        return obj.state.state_name

    def city_name(self, obj):
        return obj.city.city_name

    def active(self, obj):
        return format_html(f'''<a href="/api/v1/location/pincode/active/{obj.id}"><img src="/static/admin/img/icon-{'yes' if obj.is_active else 'no'}.svg" alt="True"></a>''')

    list_display = ['pincode', 'city_name', 'state_name', 'active', 'created_at']
    form = PincodeForm


admin.site.register(Country, CountryAdminView)
admin.site.register(State, StateAdminView)
admin.site.register(City, CityAdminView)
admin.site.register(Pincode, PincodeAdminView)
