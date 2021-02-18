from django.utils.deprecation import MiddlewareMixin
import sys
from django.http import JsonResponse
from rest_framework.response import Response
from PLR_APIs.logs import *
from .forms import *
from rest_framework.authentication import get_authorization_header
from datetime import datetime

View_class = ['company_login_view', 'index', 'login', 'media', 'serve']


class CommonMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.META['Access-Control-Allow-Origin'] = '*'
        try:
            if request.user.is_authenticated:
                return None
            if view_func.__name__ not in View_class:
                auth = get_authorization_header(request).decode()
                if auth != '':
                    if CompanyUser.objects.filter(account_id=auth, is_login=True).exists():
                        request.COOKIES['account_id'] = auth
                    else:
                        return JsonResponse({'error': "User Not Login"}, status=200)
                else:
                    return JsonResponse({'error': "User Not Login"}, status=500)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)

    # def process_exception(self, request, exception):
    #     return Response({'error': f"{exception}"}, status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = UserLoginForm(request.data)
                if not form.is_valid():
                    error = eval(form.errors.as_json())
                    print("error =-=-=-=-=-==- ", error)
                    if '__all__' in error:
                        error = error['__all__'][0]['message']
                    return Response({'error': error}, status=200)
                else:
                    return view_func(request, form)
            else:
                return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class CompanySubUserCreateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'pk' in view_kwargs:
                pk = view_kwargs['pk']
            else:
                pk = None
            if request.method == "POST":
                form = CompanySubUserCreateForm(request.data, request.FILES)
                if not form.is_valid():
                    return Response({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form, pk)
            else:
                return view_func(request, None, pk)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class UserLevelsCreateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'pk' in view_kwargs:
                pk = view_kwargs['pk']
            else:
                pk = None
            if request.method == "POST":
                form = UserLevelsCreateForm(request.data, request.FILES)
                if not form.is_valid():
                    return Response({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form, pk)
            else:
                return view_func(request, None, pk)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class UserDepartmentMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'pk' in view_kwargs:
                pk = view_kwargs['pk']
            else:
                pk = None
            if request.method == "POST":
                form = UserDepartmentForm(request.data, request.FILES)
                if not form.is_valid():
                    return Response({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form, pk)
            else:
                return view_func(request, None, pk)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class UserLogoutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        user.last_login = None
        user.is_login = False
        user.updated_at = datetime.now()
        user.save()
        return Response({'message': f"{user.username} Successfully Logout"}, status=200)
