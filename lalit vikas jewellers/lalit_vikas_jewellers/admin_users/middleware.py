from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from django.http import JsonResponse
from .models import *
import os, sys
from .forms import *
from rest_framework_simplejwt.authentication import JWTAuthentication

View_class = ['index', 'changelist_view', 'login', 'user_login_view', 'media', 'serve']


class CommonMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                return None
            if view_func.__name__ not in View_class:
                jwt_object = JWTAuthentication()
                header = jwt_object.get_header(request)
                raw_token = jwt_object.get_raw_token(header)
                validated_token = jwt_object.get_validated_token(raw_token)
                request.user = jwt_object.get_user(validated_token)
                return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = UserLoginForm(request.data, request.FILES)
                if not form.is_valid():
                    return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class UserCreateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = UserLoginForm(request.data, request.FILES)
                if not form.is_valid():
                    return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)