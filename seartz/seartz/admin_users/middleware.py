from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .forms import *
from .models import *
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

import os, sys
from rest_framework_simplejwt.authentication import JWTAuthentication


View_class = ['index', 'login_opt_send_view', 'login_opt_verify_view', 'changelist_view', 'login', 'artist_user_login_view', 'user_login_view',
              'media', 'serve', 'get_product_view', 'update_feature_product_view', 'get_product_category_view',
              'get_one_product_view', 'get_category_view', 'get_category_all_view', 'get_one_product_view', 'get_one_slug_product_view', 'home_slider_view',
              'gallery_category_view', 'contact_us_view', 'testimonial_view', 'about_us_view', 'our_team_view', 'vision_view', 'mission_view',
              'f_and_q_view', 'get_users_product_view', 'artist_login_opt_verify_view']


class CommonMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                return None
            if view_func.__name__ not in View_class:
                jwt_object = JWTAuthentication()
                header = jwt_object.get_header(request)
                if header is not None:
                    raw_token = jwt_object.get_raw_token(header)

                    validated_token = jwt_object.get_validated_token(raw_token)
                    request.user = jwt_object.get_user(validated_token)
                    if request.user.token != str(validated_token):
                        return JsonResponse({'error': "User Not Login"}, status=200)
                    return None
                return JsonResponse({'error': "Invalid Token"}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)
    #
    # def process_exception(self, request, exception):
    #     return JsonResponse({'error': f"{exception}"}, status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = UserLoginForm(request.data, request.FILES)
                if not form.is_valid():
                    error = eval(form.errors.as_json())
                    return JsonResponse({'data': None, "message": error['__all__'][0]['message'] if '__all__' in error else error, "status": 500}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class UserCreateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = AdminUsersForm(request.data, request.FILES)
                if not form.is_valid():
                    error = eval(form.errors.as_json())
                    return JsonResponse({'error': error['__all__'] if '__all__' in error else error}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class UserChangePasswordMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":

                form = UserChangePasswordsForm(request.data, request.FILES, request=request)
                if not form.is_valid():
                    return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
                else:

                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class LoginOTPSendMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = LoginOTPSendForm(request.data)
                if not form.is_valid():
                    return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class LoginOTPVerifyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = LoginOTPVerifyForm(request.data)
                if not form.is_valid():
                    return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class CreateArtistJuniorMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            form = CreateArtistJuniorForm(request.data, request.FILES)
            if not form.is_valid():
                return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
            else:
                return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class ArtistLoginOTPVerifyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            form = ArtistLoginOTPVerifyForm(request.data, request.FILES)
            if not form.is_valid():
                return JsonResponse({'error': eval(form.errors.as_json())}, status=200)
            else:
                return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)
