from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *


@api_view(['POST'])
@decorator_from_middleware(UserMiddleware)
def create_user(request, form, pk=None):
    try:
        if request.method == "POST":
            company_user_obj = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'], is_staff=True,
                                    is_active=True, is_superuser=True,)
            company_user_obj.set_password(form.cleaned_data['password'])
            company_user_obj.save()
            return Response({"data": model_to_dict(User.objects.last())}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(UserMiddleware)
def update_user(request, form, pk=None):
    try:
        if request.method == "PUT":
            user_obj = User.objects.get(id=pk)
            user_obj.username = form.cleaned_data['username']
            user_obj.email = form.cleaned_data['email']
            user_obj.set_password(form.cleaned_data['password'])
            user_obj.save()
            return Response({"data": model_to_dict(User.objects.get(id=pk))}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)
