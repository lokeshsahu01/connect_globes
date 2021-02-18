from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .forms import *


class ProductMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            pk = view_kwargs['pk'] if 'pk' in view_kwargs else None
            if request.method == "PUT":
                form = ProductForm(request.data, request.FILES, instance=Product.objects.get(id=pk))
            elif request.method == "POST":
                form = ProductForm(request.data, request.FILES)
            if not form.is_valid():
                return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
            else:
                return view_func(request, form, pk)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)
