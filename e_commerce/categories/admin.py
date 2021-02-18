from django.contrib import admin
from .models import *
from .forms import *
from django.contrib import messages


class CategoriesAdminView(admin.ModelAdmin):
    def parent_category(self, obj):
        if obj.parent:
            return obj.parent.category_name

    list_display = ['category_name', 'category_image', 'slug', 'parent_category', 'created_at']
    form = CategoriesForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoriesAdminView, self).get_form(request, obj, **kwargs)
        if obj is not None:
            if obj.category_image.name:
                form.base_fields['category_image'].help_text = f'<img src="{obj.category_image.url}" alt="Product Size Image" width="80" height="80">'
        return form

    def save_model(self, request, obj, form, change):
        try:
            if obj.id is None:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                Categories(**form.cleaned_data).save()
                cat = Categories.objects.last()
                messages.info(request, f"Category {cat.category_name} {cat.slug} Successfully Created")
            else:
                if 'category_image' in form.cleaned_data and form.cleaned_data['category_image'] and form.cleaned_data['category_image'] != '':
                    cat_obj = Categories.objects.get(id=obj.id)
                    cat_obj.category_image = form.cleaned_data['category_image']
                    cat_obj.save()
                    form.cleaned_data.pop('category_image')
                Categories.objects.filter(id=obj.id).update(**form.cleaned_data)
                messages.info(request, f"Category {obj.category_name} Successfully Updated")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


admin.site.register(Categories, CategoriesAdminView)
