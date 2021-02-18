from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from django.http import JsonResponse
from .middleware import *
from .user_info_json import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from datetime import datetime
from suit_dashboard.views import DashboardView
from django.core.files.storage import FileSystemStorage


class HomeView(DashboardView):
    pass


@api_view(['POST', ])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form=None):
    try:
        mobile = form.cleaned_data['mobile']
        password = form.cleaned_data['password']
        user_obj = User.objects.get(mobile=mobile)
        serializer = TokenObtainPairSerializer(data={'mobile': mobile, 'password': password})
        token = serializer.validate({'mobile': mobile, 'password': password})
        user_obj.token = token['access']
        user_obj.updated_at = datetime.now()
        user_obj.last_login = datetime.now()
        user_obj.save()
        user_info = user_json_info(user_obj)
        return JsonResponse({"data": user_info, "message": "Successfully Logged in", "status": 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(UserLoginMiddleware)
def artist_user_login_view(request, form=None):
    try:
        mobile = form.cleaned_data['mobile']
        password = form.cleaned_data['password']
        user_obj = User.objects.get(mobile=mobile)
        serializer = TokenObtainPairSerializer(data={'mobile': mobile, 'password': password})
        token = serializer.validate({'mobile': mobile, 'password': password})
        user_obj.token = token['access']
        user_obj.updated_at = datetime.now()
        user_obj.last_login = datetime.now()
        user_obj.save()
        user_info = user_json_info(user_obj)
        profile_data = model_to_dict(ArtistJuniorProfile.objects.get(user_id=user_obj.id))
        if 'age_proof_id_file' in profile_data:
            profile_data['age_proof_id_file'] = profile_data['age_proof_id_file'].url if profile_data['age_proof_id_file'].name else profile_data['age_proof_id_file'].name
        if 'user_image' in profile_data:
            profile_data['user_image'] = profile_data['user_image'].url if profile_data['user_image'].name else profile_data['user_image'].name
        user_info['profile'] = profile_data
        return JsonResponse({"data": user_info, "message": "Successfully Logged in", "status": 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(LoginOTPSendMiddleware)
def login_opt_send_view(request, form=None):
    try:
        response = {"data": {"mobile": form.cleaned_data['mobile'], 'user_exists': True if User.objects.filter(mobile=form.cleaned_data['mobile']).exists() else False},
                    "message": "Successfully Send OTP", "status": 200}
        return Response(response, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(LoginOTPVerifyMiddleware)
def login_opt_verify_view(request, form=None):
    try:
        mobile = form.cleaned_data['mobile']
        otp = form.cleaned_data['otp']
        password = form.cleaned_data['password']
        if not User.objects.filter(mobile=form.cleaned_data['mobile']).exists():
            account_id = None
            for i in range(5):
                rand_id = randint(10 ** (8 - 1), (10 ** 8) - 1)
                if not User.objects.filter(account_id=rand_id).exists():
                    account_id = rand_id
                    break
            if not UserRole.objects.filter(role="Buyer").exists():
                UserRole(role="Buyer").save()
            User.objects.create_user(mobile=mobile, is_mobile=True, is_active=True,
                                     account_id=account_id, user_role=UserRole.objects.get(role="Buyer").id,
                                     password=password)
        user_obj = User.objects.get(mobile=mobile)
        if password:
            serializer = TokenObtainPairSerializer(data={'mobile': mobile, 'password': password})
            token = serializer.validate({'mobile': mobile, 'password': password})['access']
        else:
            token = str(RefreshToken.for_user(user_obj).access_token)
        user_obj.token = token
        user_obj.updated_at = datetime.now()
        user_obj.last_login = datetime.now()
        user_obj.save()
        user_info = user_json_info(user_obj)
        response = {"data": user_info,
                    "message": "Successfully Login", "status": 200}
        return Response(response, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(UserChangePasswordMiddleware)
def user_password_change(request, form=None):
    try:
        request.user.set_password(form.cleaned_data['password'])
        request.user.token = None
        request.user.updated_at = datetime.now()
        request.user.save()
        return Response({'message': f'Password Successfully Changed'}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(ArtistLoginOTPVerifyMiddleware)
def artist_login_opt_verify_view(request, form=None):
    try:
        mobile = form.cleaned_data['mobile']
        password = form.cleaned_data['password']
        if not User.objects.filter(mobile=form.cleaned_data['mobile']).exists():
            account_id = None
            for i in range(5):
                rand_id = randint(10 ** (8 - 1), (10 ** 8) - 1)
                if not User.objects.filter(account_id=rand_id).exists():
                    account_id = rand_id
                    break
            if not UserRole.objects.filter(role="Artist").exists():
                UserRole(role="Artist").save()
            User.objects.create_user(email=form.cleaned_data['email'], mobile=mobile, is_mobile=True, first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'], is_active=True, account_id=account_id,
                                     user_role=UserRole.objects.get(role="Artist").id, password=password)

        user_obj = User.objects.get(mobile=mobile)
        if not ArtistJuniorProfile.objects.filter(user_id=user_obj.id):
            profile_data = {'user_id': user_obj.id, 'address': form.cleaned_data['address'],
                            'father_name': form.cleaned_data['father_name'], 'dob': form.cleaned_data['dob'],
                            'age_proof_id': form.cleaned_data['age_proof_id'], 'user_image': form.cleaned_data['user_image'],
                            'age_proof_id_file': form.cleaned_data['age_proof_id_file'], 'age_proof_id_no': form.cleaned_data['age_proof_id_no'],
                            'slug': form.cleaned_data['first_name']+'-'+form.cleaned_data['last_name'],
                            'profile_description': form.cleaned_data['user_image'], 'is_active': True}
            ArtistJuniorProfile(**profile_data).save()
        if password:
            serializer = TokenObtainPairSerializer(data={'mobile': mobile, 'password': password})
            token = serializer.validate({'mobile': mobile, 'password': password})['access']
        else:
            token = str(RefreshToken.for_user(user_obj).access_token)
        user_obj.token = token
        user_obj.updated_at = datetime.now()
        user_obj.last_login = datetime.now()
        user_obj.save()
        user_info = user_json_info(user_obj)
        profile_data = model_to_dict(ArtistJuniorProfile.objects.get(user_id=user_obj.id))
        if 'age_proof_id_file' in profile_data:
            profile_data['age_proof_id_file'] = profile_data['age_proof_id_file'].url if profile_data['age_proof_id_file'].name else profile_data['age_proof_id_file'].name
        if 'user_image' in profile_data:
            profile_data['user_image'] = profile_data['user_image'].url if profile_data['user_image'].name else profile_data['user_image'].name
        user_info['profile'] = profile_data
        return Response({"data": user_info, "message": "Successfully Login", "status": 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['PUT', ])
@decorator_from_middleware(CreateArtistJuniorMiddleware)
def create_artist_junior_view(request, form=None):
    try:
        year, month, date = datetime.now().strftime("%Y"), datetime.now().strftime("%B"), datetime.now().strftime("%d")
        user_data = {'first_name': form.cleaned_data['first_name'],
                     'last_name': form.cleaned_data['last_name']}
        profile_data = {'user_id': request.user.id, 'address': form.cleaned_data['address'],
                        'father_name': form.cleaned_data['father_name'], 'dob': form.cleaned_data['dob'],
                        'age_proof_id': form.cleaned_data['age_proof_id'],
                        'age_proof_id_no': form.cleaned_data['age_proof_id_no'], 'slug': form.cleaned_data['first_name']+'_'+form.cleaned_data['last_name'],
                        'profile_description': form.cleaned_data['user_image'], 'is_active': True}
        if 'age_proof_id_file' in form.cleaned_data and form.cleaned_data['age_proof_id_file']:
            age_proof_id_file_fs = FileSystemStorage('media/User/' + f"{year}/{month}/{date}/{form.cleaned_data['first_name']+'_'+form.cleaned_data['last_name']}")
            age_proof_id_file = age_proof_id_file_fs.save(form.cleaned_data['age_proof_id_file'].name, form.cleaned_data['age_proof_id_file'])
            profile_data['age_proof_id_file'] = 'User/' + f"{year}/{month}/{date}/{form.cleaned_data['first_name']+'_'+form.cleaned_data['last_name']}/" + age_proof_id_file
        if 'user_image' in form.cleaned_data and form.cleaned_data['user_image']:
            user_image_fs = FileSystemStorage('media/User/' + f"{year}/{month}/{date}/{form.cleaned_data['first_name']+'_'+form.cleaned_data['last_name']}")
            user_image_file = user_image_fs.save(form.cleaned_data['user_image'].name, form.cleaned_data['user_image'])
            profile_data['user_image'] = 'User/' + f"{year}/{month}/{date}/{form.cleaned_data['first_name']+'_'+form.cleaned_data['last_name']}/" + user_image_file

        User.objects.filter(id=request.user.id).update(**user_data)
        ArtistJuniorProfile.objects.filter(user_id=request.user.id).update(**profile_data)
        user_obj = model_to_dict(User.objects.get(id=request.user.id))
        profile_data = model_to_dict(ArtistJuniorProfile.objects.get(user_id=request.user.id))
        if 'age_proof_id_file' in profile_data:
            profile_data['age_proof_id_file'] = profile_data['age_proof_id_file'].url if profile_data['age_proof_id_file'].name else profile_data['age_proof_id_file'].name
            profile_data['user_image'] = profile_data['user_image'].url if profile_data['user_image'].name else profile_data['user_image'].name
        user_obj['profile'] = profile_data
        user_obj.pop('password')
        return Response({'data': user_obj, 'message': f'Successfully Changed User Profile'}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


@api_view(['GET', ])
def get_artist_junior_view(request):
    try:
        user_obj = model_to_dict(request.user)
        profile_data = model_to_dict(ArtistJuniorProfile.objects.get(user_id=request.user.id))
        if 'age_proof_id_file' in profile_data:
            profile_data['age_proof_id_file'] = profile_data['age_proof_id_file'].url if profile_data['age_proof_id_file'].name else profile_data['age_proof_id_file'].name
            profile_data['user_image'] = profile_data['user_image'].url if profile_data['user_image'].name else profile_data['user_image'].name
        user_obj['profile'] = profile_data
        return Response({'data': user_obj, 'message': f'Successfully Changed User Profile'}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)
