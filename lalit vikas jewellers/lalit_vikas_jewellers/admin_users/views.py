from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from .user_info_json import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@api_view(['POST', ])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form=None):
    try:
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_info = user_json_info(User.objects.get(username=username))
        serializer = TokenObtainPairSerializer(data={'username': username, 'password': password})
        token = serializer.validate({'username': username, 'password': password})
        user_info['token'] = token['access']
        return Response(user_info, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(UserCreateMiddleware)
def home_view(request):
    try:
        return Response({"message": "This is home page"}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)