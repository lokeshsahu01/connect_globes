from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin
from PLR_APIs.logs import *
from .forms import *
import sys
import os


class AllFoldersMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'pk' in view_kwargs:
                pk = view_kwargs['pk']
            else:
                pk = None
            if request.method == "POST":
                request.data['account_id'] = request.COOKIES['account_id']
                form = AllFoldersForm(request.data)
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


class CreateDMSMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = CreateDMSForm(request.POST)
                if not form.is_valid():
                    return Response({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


class DMSMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'pk' in view_kwargs:
                pk = view_kwargs['pk']
            else:
                pk = None
            if request.method == "POST":
                form = AllFoldersForm(request.data)
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
