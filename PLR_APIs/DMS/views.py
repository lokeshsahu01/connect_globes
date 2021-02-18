from .middleware import *
from django.utils.decorators import decorator_from_middleware
from .serializers import *
from rest_framework.decorators import api_view, renderer_classes
from django.conf import settings
import shutil
from django.forms.models import model_to_dict
from django.db.models import Max


@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(AllFoldersMiddleware)
def folder_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if pk is not None:
            folder_obj = AllFolders.objects.get(id=pk)
            folder_path = upper_tree_folder(folder_obj) + folder_obj.folder_name
            if user.is_company:
                user_path = os.path.join(settings.MEDIA_ROOT.replace('\\', '/') + f"/plr/{str(user.username)}/Documents{folder_path}")
            else:
                user_path = os.path.join(settings.MEDIA_ROOT.replace('\\', '/') + f"/plr/{str(user.company_sub_user_id.username)}/{str(user.username)}/Documents{folder_path}")
        if request.method == "POST":
            form.cleaned_data['user'] = str(user.id)
            if form.cleaned_data['parent_id'] == '' or form.cleaned_data['parent_id'] is None:
                form.cleaned_data.pop('parent_id')
            if pk is not None:
                folder_obj = AllFolders.objects.get(id=pk)
                serializer = AllFoldersSerializer(instance=folder_obj, data=form.cleaned_data)
                rename_path = user_path.split('/')
                if rename_path[-1] == '':
                    rename_path[-2] = form.cleaned_data['folder_name']
                else:
                    rename_path[-1] = form.cleaned_data['folder_name']
                rename_path = '/'.join(rename_path)
                os.rename(user_path, rename_path)
            else:
                serializer = AllFoldersSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
        elif request.method == "DELETE":
            if pk is not None:
                shutil.rmtree(user_path)
                tree_folder = lower_tree_folder(folder_obj)
                if tree_folder:
                    child_folder = [i.delete() for i in tree_folder]
                folder_obj.delete()
                return Response(user_path, status=200)
        else:
            if pk is not None:
                folder_obj = lower_tree_folder(AllFolders.objects.get(id=pk))
                folder_obj.insert(0, AllFolders.objects.get(id=pk))
            else:
                folder_obj = AllFolders.objects.filter(user=user)
            serializer = AllFoldersSerializer(instance=folder_obj, many=True)
            return Response(serializer.data, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['POST'])
@decorator_from_middleware(CreateDMSMiddleware)
def create_dms_view(request, form=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])

        if request.method == "POST":
            form.cleaned_data['user'] = str(user.id)
            if 'upload_file[]' not in request.FILES and request.FILES.getlist('upload_file[]') is None and not any(request.FILES.getlist('upload_file[]')):
                return Response({'error': "Document File Required"}, status=200)
            response_data = []
            response_error = []
            for i in request.FILES.getlist('upload_file[]'):
                form.cleaned_data['upload_file'] = i
                form.cleaned_data['file_name'] = i.name

                if len(request.FILES.getlist('upload_file[]')) > 1:
                    upload_type = 'Batch'
                    getbatch = ScanFile.objects.filter(user_id=user, upload_type=upload_type).aggregate(Max('batch_no'))
                    if getbatch['batch_no__max'] is not None:
                        batch_no = getbatch['batch_no__max'] + 1
                    else:
                        batch_no = 1
                else:
                    upload_type = 'Single'
                    batch_no = 0
                form.cleaned_data['upload_type'] = upload_type
                form.cleaned_data['batch_no'] = batch_no
                serializer = DMSSerializer(data=form.cleaned_data)
                if serializer.is_valid():
                    serializer.save()
                    if 'file_tag' in form.cleaned_data and form.cleaned_data['file_tag'] != '' and form.cleaned_data['file_tag'] is not None:
                        file_tag_serializer = FileTagSerializer(data={'user': str(user.id),
                                                                      'file_id': str(ScanFile.objects.last().id),
                                                                      'file_tag': form.cleaned_data['file_tag']
                                                                      })
                        if file_tag_serializer.is_valid():
                            file_tag_serializer.save()
                            serializer.data['file_tag'] = file_tag_serializer.data
                    response_data.append(serializer.data)
                else:
                    response_error.append(serializer.errors)
            if any(response_error):
                return Response(response_error, status=200)
            else:
                return Response(response_data, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(DMSMiddleware)
def dms_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if request.method == "POST":
            if pk:
                instance = ScanFile.objects.get(id=pk, user=user, status=True)
                serializer = DMSSerializer(instance=instance, data=form.cleaned_data)
                if serializer.is_valid():
                    serializer.save()
                    if 'file_tag' in form.cleaned_data and form.cleaned_data['file_tag'] != '' and form.cleaned_data['file_tag'] is not None:
                        file_tag_serializer = FileTagSerializer(data={'user': str(user.id),
                                                                      'file_id': str(instance.id),
                                                                      'file_tag': form.cleaned_data['file_tag']
                                                                      })
                        if file_tag_serializer.is_valid():
                            file_tag_serializer.save()
                            serializer.data['file_tag'] = file_tag_serializer.data
                    return Response(serializer.data, status=200)
        elif request.method == "DELETE":
            if pk:
                instance = ScanFile.objects.get(id=pk, user=user, status=True)
                filename = instance.file_name
                if instance.upload_file:
                    if os.path.isfile(instance.upload_file.path):
                        os.remove(instance.upload_file.path)
                if FileTag.objects.filter(file_id=instance, user=user).exists():
                    FileTag.objects.filter(file_id=instance, user=user).delete()
                instance.delete()
                return Response(f'{filename} successfully deleted', status=200)
            else:
                return Response(f'Unique id is required', status=200)
        else:
            if pk:
                instance = ScanFile.objects.get(id=pk, user=user, status=True)
                many = False
            else:
                instance = ScanFile.objects.filter(user=user, status=True)
                many = True
            scan_serializer = DMSSerializer(instance=instance, many=many)
            print(scan_serializer.data, type(scan_serializer.data))
            return Response(scan_serializer.data, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)
