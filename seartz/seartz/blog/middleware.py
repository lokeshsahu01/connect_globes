from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .forms import *
import os
import sys


class CreateBlogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = CreateBlogForm(request.data, request.FILES)
                if not form.is_valid():
                    error = eval(form.errors.as_json())
                    return JsonResponse({'error': error['__all__'] if '__all__' in error else error}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class CreateBlogCommentMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = CreateBlogCommentForm(request.data, request.FILES)
                if not form.is_valid():
                    error = eval(form.errors.as_json())
                    return JsonResponse({'error': error['__all__'] if '__all__' in error else error}, status=200)
                else:
                    return view_func(request, form, view_kwargs['blog_id'])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)