from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages
from .hierarchical_category import *
from django.utils.html import format_html
from product.models import *


class CategoriesAdminView(admin.ModelAdmin):
    def sub_categories(self, obj):
        if obj.sub_category is None:
            return None
        self.sub_category = Categories.objects.get(id=obj.sub_category)
        return format_html(f'<a href="/admin/categories/categories/{self.sub_category.id}/change/" target="_blank">{self.sub_category.category_name}</a>')

    def get_slug(self, obj):
        url = '/'.join(i for i in parent_tree_category(obj).split('/')[::-1])
        return format_html(f'<a href="/api/v1/category/urls/{url}" target="_blank">{obj.category_name.lower()}</a>')

    def product_count(self, obj):
        count = Product.objects.filter(category_id=obj.id).count()
        if count:
            url = f"/admin/product/product/?category__id__exact={obj.id}"
        else:
            url = "#"
        return format_html(f'<a href={url}>{count}</a>')

    def category_image_(self, obj):
        if obj.category_image.name != '' and obj.category_image.name is not None:
            return format_html(f'<img src="{obj.category_image.url}" alt="Product Size Image" width="50" height="50">')

    list_display = ['category_name', 'category_image_', 'get_slug', 'sub_categories', 'product_count', 'created_at']
    form = CategoriesForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoriesAdminView, self).get_form(request, obj, **kwargs)
        if obj is None:
            for key in ['slug', 'meta_description', 'meta_keyword']:
                del form.base_fields[key]
            form.base_fields['category_image'].help_text = ""
            form.base_fields['category'].choices = get_categories(True)
        else:
            categories = get_categories(True)
            for i in categories:
                if ' ' + obj.category_name in i:
                    categories.remove(i)
            form.base_fields['category'].choices = categories
            if obj.sub_category is not None:
                form.base_fields['category'].initial = Categories.objects.get(id=obj.sub_category).category_name
            if obj.category_image.name != '' and obj.category_image.name is not None:
                form.base_fields['category_image'].help_text = f'<img src="{obj.category_image.url}" alt="Product Size Image" width="80" height="80">'
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                Categories(**form.cleaned_data).save()
                cat = Categories.objects.last()
                messages.info(request, f"Category {cat.category_name} {cat.slug} Successfully Created")
            else:
                if 'category_image' in form.cleaned_data and form.cleaned_data['category_image'] and form.cleaned_data['category_image'] != '':
                    prod_obj = Categories.objects.get(id=obj.id)
                    prod_obj.category_image = form.cleaned_data['category_image']
                    prod_obj.save()
                    del form.cleaned_data['category_image']
                Categories.objects.filter(id=obj.id).update(**form.cleaned_data)
                messages.info(request, f"Category {obj.category_name} Successfully Updated")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(Categories, CategoriesAdminView)
