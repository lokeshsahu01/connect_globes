from .middleware import *
from django.utils.decorators import decorator_from_middleware
from .serializers import *
from datetime import datetime
from rest_framework.decorators import api_view
from .in_json import *
from .models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def company_login_view(request, form):
    try:
        user = CompanyUser.objects.get(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        user.last_login = datetime.now()
        user.is_login = True
        user.updated_at = datetime.now()
        user.save()
        return Response({'message': f"{user.username} Successfully Login", "account_id": user.account_id}, status=200)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(CompanySubUserCreateMiddleware)
def company_sub_user_create_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if user.is_company:
            if request.method == "POST":
                form.cleaned_data['email'] = request.POST.get('email')
                if pk is None and CompanyUser.objects.filter(username=form.cleaned_data['username'], company_sub_user_id=user).exists():
                    return Response({'error': f"Username {form.cleaned_data['username']} is Already exists !!!"},
                                    status=500)
                if pk is None and CompanyUser.objects.filter(email=form.cleaned_data['email']).exists():
                    return Response({'error': f"Email {form.cleaned_data['email']} is Already exists !!!"}, status=500)

                form.cleaned_data['is_company'] = False
                if 'password' in form.cleaned_data and form.cleaned_data['password'] is not None or form.cleaned_data['password'] != "":
                    form.cleaned_data['password'] = 'pbkdf2_sha256$180000$' + hashlib.sha256(
                        form.cleaned_data["password"].encode()).hexdigest()
                form.cleaned_data['company_sub_user_id'] = user.id
                form.cleaned_data['name'] = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
                form.cleaned_data['company_id'] = user.id
                instance = CompanyUser.objects.get(id=pk, company_sub_user_id=user) if pk else None
                instance2 = CompanySubUser.objects.get(user=instance) if pk else None

                if pk is None:
                    if CompanyDetails.objects.filter(user=user).exists():
                        if not CompanyUser.objects.filter(company_sub_user_id=user).count() <= CompanyDetails.objects.get(user=user).allowed_user:
                            return Response(
                                {'error': f"User Limit Reached {CompanyDetails.objects.get(user=user).allowed_user}"},
                                status=500)

                    for i in range(5):
                        random = randint(10 ** (8 - 1), (10 ** 8) - 1)
                        if not CompanyUser.objects.filter(account_id=random).exists():
                            form.cleaned_data['account_id'] = random
                            break
                else:
                    form.cleaned_data.pop('username')
                    form.cleaned_data.pop('email')
                    if 'user_image' in form.cleaned_data:
                        if instance2.user_image:
                            if os.path.isfile(instance2.user_image.path):
                                os.remove(instance2.user_image.path)
                    form.cleaned_data['is_deactivate'] = True
                serialize = CompanyUserSerializer(instance=instance, data=form.cleaned_data)
                if serialize.is_valid():
                    serialize.save()
                    form.cleaned_data['user'] = CompanyUser.objects.get(username=serialize.data['username'],
                                                                        company_sub_user_id=user).id
                    serializer = SubUserCompanyDetailsSerializer(instance=instance2, data=form.cleaned_data)
                    if serializer.is_valid():
                        serializer.save()
                        d = serializer.data
                        d.update(serialize.data)
                        d.pop('password')
                        return Response(d, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                else:
                    return Response(serialize.errors, status=400)
            else:
                if pk:
                    instance = CompanyUser.objects.get(id=pk)
                    serializer = CompanyUserSerializer(instance=instance, many=False)
                    get_serialize = SubUserCompanyDetailsSerializer(instance=CompanySubUser.objects.get(user=instance),
                                                                    many=False)
                    d = serializer.data
                    d.update(get_serialize.data)
                    d.pop('password')
                    return Response(d, status=200)
                else:
                    user_list = []
                    instance = CompanyUser.objects.filter(company_sub_user_id=user)

                    for i in CompanySubUser.objects.filter(user__in=instance):
                        k = model_to_dict(i)
                        k['user_level'] = i.user_level.level_name
                        k['user_department'] = i.user_department.department_name
                        k['created_at'] = i.created_at
                        if 'user_image' in k and k['user_image'] is not None:
                            k['user_image'] = i.user_image.name
                        user_list.append(k)
                    return JsonResponse(user_list, safe=False)
        else:
            return Response({'error': f"{user.username} is not company user so he cannot create the user"}, status=500)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET', ])
def get_total_user(request):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if user.is_company:
            if CompanyDetails.objects.filter(user=user).exists():
                total_user = CompanyDetails.objects.get(user=user).allowed_user
                count_user = CompanyUser.objects.filter(company_sub_user_id=user).count()
                return JsonResponse({'total_user': total_user, 'count_user': count_user}, status=200)
            else:
                return Response({'error': f"Company user`s Detail not Available "}, status=500)
        else:
            return Response({'error': "User is not Company User"}, status=500)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(UserLevelsCreateMiddleware)
def create_user_level_view(request, form=None, pk=None):
    user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
    if user.is_company:
        if request.method == "POST":
            form.cleaned_data['user'] = str(user.id)
            if pk:
                user_level = UserLevels.objects.get(id=pk)
                serialize = UserLevelsCreateSerializer(instance=user_level, data=form.cleaned_data)
            else:
                serialize = UserLevelsCreateSerializer(data=form.cleaned_data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=200)
            else:
                return Response(serialize.errors, status=400)
        elif request.method == "DELETE":
            user_level = UserLevels.objects.get(id=pk)
            user_level_name = user_level.level_name
            user_level.delete()
            return Response({'message': f'{user_level_name} successfully deleted'}, status=200)
        else:
            if pk:
                user_level = UserLevels.objects.get(id=pk)
                many = False
            else:
                user_level = UserLevels.objects.filter(user=user)
                many = True
            serialize = UserLevelsCreateSerializer(user_level, many=many)

            return Response(serialize.data, status=200)


@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(UserDepartmentMiddleware)
def user_department_view(request, form=None, pk=None):
    user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
    if user.is_company:
        if request.method == "POST":
            form.cleaned_data['user'] = str(user.id)
            if pk:
                user_department = UserDepartment.objects.get(id=pk)
                serialize = UserDepartmentSerializer(instance=user_department, data=form.cleaned_data)
            else:
                serialize = UserDepartmentSerializer(data=form.cleaned_data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=200)
            else:
                return Response(serialize.errors, status=400)
        elif request.method == "DELETE":
            user_department = UserDepartment.objects.get(id=pk)
            user_department_name = user_department.department_name
            user_department.delete()
            return Response({'message': f'{user_department_name} successfully deleted'}, status=200)
    if request.method == "GET":
        if pk:
            user_department = UserDepartment.objects.get(id=pk)
            many = False
        else:
            user = user if user.is_company else user.company_sub_user_id
            user_department = UserDepartment.objects.filter(user=user)
            many = True
        serialize = UserDepartmentSerializer(user_department, many=many)

        return Response(serialize.data, status=200)


@api_view(['POST'])
def user_activate_view(request, pk):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if user.is_company:
            if request.method == "POST":
                if CompanySubUser.objects.filter(user=CompanyUser.objects.get(id=pk)).exists():
                    user = CompanySubUser.objects.get(user=CompanyUser.objects.get(id=pk))
                    if user.is_deactivate:
                        user.is_deactivate = False
                    else:
                        user.is_deactivate = True
                    user.save()
                    k = model_to_dict(user)
                    k['user_level'] = user.user_level.level_name
                    k['user_department'] = user.user_department.department_name
                    k['created_at'] = user.created_at
                    if 'user_image' in k and k['user_image'] is not None:
                        k['user_image'] = user.user_image.name
                    return JsonResponse(k, safe=False)
                else:
                    return Response({'error': 'User Not Found'}, status=200)
        else:
            return Response({'error': 'User Is Not Company Owner'}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET'])
@decorator_from_middleware(UserLogoutMiddleware)
def user_logout_view(request):
    pass
