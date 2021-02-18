from django.utils.deprecation import MiddlewareMixin
import os
import sys
from rest_framework.response import Response
from .forms import *
from django.forms.models import model_to_dict


class UserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'pk' in view_kwargs:
                pk = view_kwargs['pk']
            else:
                pk = None
            if request.method == "POST":
                form = UserForm(request.data, request.FILES)
                if not form.is_valid():
                    return Response({'error': eval(form.errors.as_json())}, status=200)
                else:
                    return view_func(request, form, pk)
            else:
                return view_func(request, None, pk)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)