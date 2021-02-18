from .middleware import *
from django.utils.decorators import decorator_from_middleware
from .serializers import *
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime, timedelta
from .tms_json import *
from django.utils import timezone
from django.http import JsonResponse


@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(GroupMiddleware)
def group_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        lower_tree_user = child_tree_users(user)
        upper_tree_user = parent_tree_users(user)
        all_user = []
        all_user.extend(lower_tree_user)
        all_user.extend(upper_tree_user)
        if request.method == "POST":
            if pk is None and Group.objects.filter(group_name=form.cleaned_data['group_name'], created_by__in=all_user).exists():
                return Response({'error': f"Group Name {form.cleaned_data['group_name']} is Already exists !!!"},
                                status=500)
            form.cleaned_data['selected_user_list'] = eval(form.cleaned_data['selected_user_list'])
            for i in form.cleaned_data['selected_user_list']:
                if CompanyUser.objects.filter(id=int(i)).exists():
                    if not CompanyUser.objects.get(id=int(i)) in lower_tree_user:
                        return Response({'error': f"User id {i} selection is not correct"}, status=500)
                else:
                    return Response({'error': f"User id {i} Not Exists !!!"}, status=500)
            form.cleaned_data['created_by'] = str(user.id)
            form.cleaned_data['total_user'] = len(form.cleaned_data['selected_user_list'])
            form.cleaned_data['selected_user_list'] = str(form.cleaned_data['selected_user_list'])
            if pk:
                group_obj = Group.objects.get(id=pk)
                serialize = GroupSerializer(instance=group_obj, data=form.cleaned_data)
                logs_serializer = TaskActivityLogsSerializer(data={'user': str(user.id), 'log_type': 'INFO',
                                                                   'log_description': f"{user.username} Update Group {form.cleaned_data['group_name']}"})
            else:
                serialize = GroupSerializer(data=form.cleaned_data)
                logs_serializer = TaskActivityLogsSerializer(data={'user': str(user.id), 'log_type': 'INFO',
                                                                   'log_description': f"{user.username} create Group {form.cleaned_data['group_name']}"})
            if serialize.is_valid() and logs_serializer.is_valid():
                serialize.save()
                logs_serializer.save()
                return Response(serialize.data, status=200)
            else:
                return Response(serialize.errors, status=400)
        elif request.method == "DELETE":
            group = Group.objects.get(id=pk)
            group_name = group.group_name
            group.delete()
            return Response({'message': f'{group_name} successfully deleted'}, status=200)
        else:
            if pk:
                group_obj = Group.objects.get(id=pk)
                many = False
            else:
                group_obj = Group.objects.filter(created_by=user)
                many = True
            serialize = GroupSerializer(group_obj, many=many)

            return Response(serialize.data, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['POST', 'DELETE'])
@decorator_from_middleware(TaskMiddleware)
def task_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if request.method == "POST":
            lower_tree_user = child_tree_users(user)
            lower_tree_user = lower_tree_user if lower_tree_user else []
            if any(lower_tree_user):
                if form.cleaned_data['assigned_to_user'] is not None and form.cleaned_data['assigned_to_user'] and not CompanyUser.objects.get(id=form.cleaned_data['assigned_to_user']) in lower_tree_user:
                    return Response({"error": "You are not assigning Under your user."}, status=500)
                form.cleaned_data['user'] = str(user.id)
                form.cleaned_data['task_type'] = '2' if 'document_file' in form.cleaned_data and form.cleaned_data['document_file'] is not None else '1'
                if pk:
                    if Task.objects.filter(id=pk, user=user).exists():
                        instance = Task.objects.get(id=pk, user=user)
                        task_serializer = TaskSerializer(instance=instance, data=form.cleaned_data)
                        logs_serializer = TaskActivityLogsSerializer(
                            data={'user': str(user.id), 'log_type': 'INFO',
                                  'log_description': f"""{user.username} Update Task {form.cleaned_data['task_title']}"""})
                    else:
                        return Response({'error': f'Task Id {pk} is not Exists'}, status=500)
                else:
                    form.cleaned_data['status'] = "Open"
                    task_serializer = TaskSerializer(data=form.cleaned_data)
                    logs_serializer = TaskActivityLogsSerializer(
                        data={'user': str(user.id), 'log_type': 'INFO',
                              'log_description': f"""{user.username} Created Task {form.cleaned_data['task_title']}"""})
                if task_serializer.is_valid() and logs_serializer.is_valid():
                    task_serializer.save()
                    logs_serializer.save()
                    task_onj = Task.objects.get(id=pk, user=user) if pk else Task.objects.filter(user=user).last()
                    form.cleaned_data['task'] = str(task_onj.id)
                    if 'attached_resources' in form.cleaned_data and form.cleaned_data['attached_resources'] != '' and form.cleaned_data['attached_resources'] is not None:
                        form.cleaned_data['file_name'] = form.cleaned_data['attached_resources'].name
                        form.cleaned_data['file_size'] = form.cleaned_data['attached_resources'].size
                        if TaskFileManagement.objects.filter(task=task_onj).exists():
                            task_file_obj = TaskFileManagement.objects.filter(task=task_onj)
                            form.cleaned_data['is_same_file'] = task_file_obj[0].id
                            form.cleaned_data['file_version'] = task_file_obj.order_by('-id')[0].file_version + 1
                        else:
                            form.cleaned_data['is_same_file'] = None
                            form.cleaned_data['file_version'] = 1
                        task_file_serializer = TaskFileManagementSerializer(data=form.cleaned_data)
                        if task_file_serializer.is_valid():
                            task_file_serializer.save()
                        else:
                            return Response(task_file_serializer.errors, status=500)

                    if 'comment' in form.cleaned_data and form.cleaned_data['comment'] is not None and form.cleaned_data['comment'] != '':
                        task_comment_serializer = TaskCommentSerializer(data=form.cleaned_data)
                        if task_comment_serializer.is_valid():
                            task_comment_serializer.save()
                        else:
                            return Response(task_comment_serializer.errors, status=500)
                    json_task = {}
                    json_task['Task'] = single_task_json(task_onj)
                    task_file_management_list = []
                    if TaskFileManagement.objects.filter(task=task_onj).exists():
                        for i in TaskFileManagement.objects.filter(task=task_onj):
                            files = model_to_dict(i)
                            files['attached_resources'] = i.attached_resources.name
                            files['user'] = i.user.username
                            task_file_management_list.append(files)
                    json_task['Task_File_Management'] = task_file_management_list
                    task_comment_list = []
                    if TaskComment.objects.filter(task=task_onj).exists():
                        for k in TaskComment.objects.filter(task=task_onj):
                            comment = model_to_dict(k)
                            comment['user'] = k.user.username
                            task_comment_list.append(comment)
                    json_task['Task_Comment'] = task_comment_list
                    return Response(json_task, status=200)
                else:
                    return Response(task_serializer.errors, status=500)
            else:
                return Response({"error": "User is last in user tree. So he can`t create task"}, status=500)
        elif request.method == "DELETE":
            if pk:
                task_obj = Task.objects.get(id=pk)
                task_file_obj = TaskFileManagement.objects.filter(task=task_obj)
                for i in task_file_obj:
                    if i.attached_resources:
                        if os.path.isfile(i.attached_resources.path):
                            os.remove(i.attached_resources.path)
                task_file_obj.delete()
                TaskComment.objects.filter(task=task_obj).delete()
                task_title = task_obj.task_title
                task_obj.delete()
                logs_serializer = TaskActivityLogsSerializer(
                    data={'user': str(user.id), 'log_type': 'INFO',
                          'log_description': f"""{user.username} Created Task {task_title}"""})
                if logs_serializer.is_valid():
                    logs_serializer.save()
                    return Response({'message': f'{task_title} successfully deleted'}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET'])
def get_task_view(request, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        lower_tree_user = child_tree_users(user)
        if pk:

            if not Task.objects.filter(id=pk).exists():
                return Response({"error": "Task is not exists"}, status=500)
            task_list = {}
            task_obj = Task.objects.get(id=pk)
            task_json = single_task_json(task_obj)
            task_list['Task'] = task_json
            task_file_management_list = []
            if TaskFileManagement.objects.filter(task=task_obj).exists():
                for i in TaskFileManagement.objects.filter(task=task_obj):
                    files = model_to_dict(i)
                    files['attached_resources'] = i.attached_resources.name
                    files['user'] = i.user.username
                    task_file_management_list.append(files)
            task_list['Task_File_Management'] = task_file_management_list
            task_comment_list = []
            if TaskComment.objects.filter(task=task_obj).exists():
                for k in TaskComment.objects.filter(task=task_obj):
                    comment = model_to_dict(k)
                    comment['user'] = k.user.username
                    task_comment_list.append(comment)
            task_list['Task_Comment'] = task_comment_list
            return Response(task_list, status=200)

        if user.is_company:
            today_due_task = Task.objects.filter(user__in=lower_tree_user, start_date__lte=datetime.now(),
                                                 due_date__gte=datetime.now())
            finished_task = Task.objects.filter(user__in=lower_tree_user, due_date__lte=datetime.now(),
                                                status='Done')
            upcoming_task = Task.objects.filter(user__in=lower_tree_user, start_date__gte=datetime.now())
            overdue_task = Task.objects.filter(user__in=lower_tree_user, status__in=['Open', 'In Progress'],
                                               due_date__lte=datetime.now())
            shared_by_me_task = Task.objects.filter(user=user)
            shared_to_me_task_user = None
        else:
            department = CompanySubUser.objects.get(user=user)
            today_due_task = Task.objects.filter(Q(assigned_to_user=user) | Q(
                assigned_to_group__in=Group.objects.filter(selected_user_list__contains=user.id)) | Q(
                user_department=department.user_department),
                                                 start_date__lte=datetime.now(),
                                                 due_date__gte=datetime.now(), status__in=['Open', 'In Progress'])
            finished_task = Task.objects.filter(Q(assigned_to_user=user) | Q(
                assigned_to_group__in=Group.objects.filter(selected_user_list__contains=user.id)) | Q(
                user_department=department.user_department),
                                                Q(due_date__lte=datetime.now()) | Q(status='Done'))
            upcoming_task = Task.objects.filter(Q(assigned_to_user=user) | Q(
                assigned_to_group__in=Group.objects.filter(selected_user_list__contains=user.id)) | Q(
                user_department=department.user_department),
                                                start_date__gte=datetime.now(), status__in=['Open', 'In Progress'])
            overdue_task = Task.objects.filter(Q(assigned_to_user=user) | Q(
                assigned_to_group__in=Group.objects.filter(selected_user_list__contains=user.id)) | Q(
                user_department=department.user_department),
                                               status__in=['Open', 'In Progress'], due_date__lte=datetime.now())
            shared_by_me_task = Task.objects.filter(user=user)

            shared_to_me_task_user = Task.objects.filter(user__in=lower_tree_user)
            shared_to_me_task_user = task_in_json(shared_to_me_task_user) if shared_to_me_task_user else []
        params = {'today_due_task': task_in_json(today_due_task), 'finished_task': task_in_json(finished_task),
                  'upcoming_task': task_in_json(upcoming_task), 'overdue_task': task_in_json(overdue_task),
                  'shared_by_me_task': task_in_json(shared_by_me_task),
                  'shared_to_me_task': shared_to_me_task_user}
        return Response(params, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['POST',])
@decorator_from_middleware(ReassignTaskMiddleware)
def reassign_task_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if request.method == "POST":
            if pk:
                if Task.objects.filter(id=pk, user=user).exists():
                    instance = Task.objects.get(id=pk, user=user)
                    instance.assigned_type = form.cleaned_data['assigned_type']
                    instance.assigned_to_user = CompanyUser.objects.get(id=form.cleaned_data['assigned_to_user']) if \
                    form.cleaned_data['assigned_to_user'] else None
                    instance.assigned_to_group = Group.objects.get(id=form.cleaned_data['assigned_to_group']) if \
                    form.cleaned_data['assigned_to_group'] else None
                    instance.user_department = UserDepartment.objects.get(id=form.cleaned_data['user_department']) if \
                    form.cleaned_data['user_department'] else None
                    instance.updated_at = datetime.now()
                    instance.save()
                    task_list = {}
                    task_obj = Task.objects.get(id=pk, user=user)
                    task_json = single_task_json(task_obj)
                    task_list['Task'] = task_json
                    task_file_management_list = []
                    if TaskFileManagement.objects.filter(task=task_obj).exists():
                        for i in TaskFileManagement.objects.filter(task=task_obj):
                            files = model_to_dict(i)
                            files['attached_resources'] = i.attached_resources.name
                            files['user'] = i.user.username
                            task_file_management_list.append(files)
                    task_list['Task_File_Management'] = task_file_management_list
                    task_comment_list = []
                    if TaskComment.objects.filter(task=task_obj).exists():
                        for k in TaskComment.objects.filter(task=task_obj):
                            comment = model_to_dict(k)
                            comment['user'] = k.user.username
                            task_comment_list.append(comment)
                    task_list['Task_Comment'] = task_comment_list
                    return Response(task_list, status=200)
                else:
                    return Response({'error': 'Task Is Not Exists'}, status=500)
            else:
                return Response({'error': 'Task Id required'}, status=500)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)

@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(TaskCommentMiddleware)
def task_comment_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if request.method == "POST":
            form.cleaned_data['user'] = str(user.id)
            if pk:
                task_comment_obj = TaskComment.objects.get(id=pk, user=user, task=form.cleaned_data['task'])
                if task_comment_obj.created_at + timedelta(hours=12) > timezone.now():
                    task_comment_serializer = TaskCommentSerializer(instance=task_comment_obj, data=form.cleaned_data)
                else:
                    Response({'error': f"Task Comment Can`t Edit"}, status=500)
            else:
                task_comment_serializer = TaskCommentSerializer(data=form.cleaned_data)

            if task_comment_serializer.is_valid():
                task_comment_serializer.save()
                task_obj = TaskComment.objects.filter(task=form.cleaned_data['task']).last()
                logs_serializer = TaskActivityLogsSerializer(
                    data={'user': str(user.id), 'log_type': 'INFO',
                          'log_description': f"""{user.username} Add Comment On Task {task_obj.task.task_title}"""})
                if logs_serializer.is_valid():
                    logs_serializer.save()
                tsk = model_to_dict(task_obj)
                tsk['user'] = task_obj.user.username
                tsk['created_at'] = task_obj.created_at
                return Response(tsk, status=200)
        elif request.method == "DELETE":
            task_comment_obj = TaskComment.objects.get(id=pk, user=user)
            task_title = task_comment_obj.task.task_title
            task_obj = task_comment_obj.task
            if task_comment_obj.created_at + timedelta(hours=12) > timezone.now():
                task_comment_obj.delete()
                logs_serializer = TaskActivityLogsSerializer(
                    data={'user': str(user.id), 'log_type': 'INFO',
                          'log_description': f"""{user.username} Deleted Comment On Task {task_title}"""})
                if logs_serializer.is_valid():
                    logs_serializer.save()
                return Response(TaskCommentSerializer(instance=TaskComment.objects.filter(task=task_obj),
                                                      many=True).data, status=200)

            else:
                Response({'error': f"Task Comment Can`t Delete"}, status=500)
        else:
            comment_list = []
            if TaskComment.objects.filter(task=Task.objects.get(id=request.GET['task'])).exists():
                for i in TaskComment.objects.filter(task=Task.objects.get(id=request.GET['task'])):
                    comment_json = model_to_dict(i)
                    comment_json['user'] = i.user.username
                    comment_list.append(comment_json)
            return Response(comment_list, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET', 'POST', 'DELETE'])
@decorator_from_middleware(TaskFileManagementMiddleware)
def task_file_management_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if request.method == "POST":
            form.cleaned_data['user'] = str(user.id)
            form.cleaned_data['file_name'] = form.cleaned_data['attached_resources'].name
            form.cleaned_data['file_size'] = form.cleaned_data['attached_resources'].size
            task_file_serializer = TaskFileManagementSerializer(data=form.cleaned_data)
            if task_file_serializer.is_valid():
                task_file_serializer.save()
                task_obj = TaskFileManagement.objects.filter(task=form.cleaned_data['task']).last()
                logs_serializer = TaskActivityLogsSerializer(
                    data={'user': str(user.id), 'log_type': 'INFO',
                          'log_description': f"""{user.username} Add File On Task {task_obj.task.task_title}"""})
                if logs_serializer.is_valid():
                    logs_serializer.save()
                k = task_file_serializer.data
                k['attached_resources'] = task_obj.attached_resources.name
                k['user'] = task_obj.user.username
                return Response(k, status=200)
            else:
                return Response(task_file_serializer.errors, status=500)

        elif request.method == "DELETE":
            if pk:
                task_file_obj = TaskFileManagement.objects.get(id=pk)
                file_name = task_file_obj.file_name
                task_obj = task_file_obj.task
                if task_file_obj.attached_resources:
                    if os.path.isfile(task_file_obj.attached_resources.path):
                        os.remove(task_file_obj.attached_resources.path)
                task_file_obj.delete()
                logs_serializer = TaskActivityLogsSerializer(
                    data={'user': str(user.id), 'log_type': 'INFO',
                          'log_description': f"""{user.username} Delete File {file_name} On Task {task_obj.task_title}"""})
                if logs_serializer.is_valid():
                    logs_serializer.save()
                task_obj = TaskFileManagement.objects.filter(task=task_obj)
                return Response(TaskFileManagementSerializer(instance=task_obj, many=True).data, status=200)
        else:
            if pk:
                task_file_obj = TaskFileManagement.objects.get(id=pk)
                task_file_json = model_to_dict(task_file_obj)
                task_file_json['attached_resources'] = task_file_obj.attached_resources.name
                task_file_json['user'] = task_file_obj.user.username
                task_file_json['created_at'] = task_file_obj.created_at
            else:
                task_file_json = []
                for i in TaskFileManagement.objects.filter(task=Task.objects.get(id=request.GET['task'])):
                    k = model_to_dict(i)
                    k['attached_resources'] = i.attached_resources.name
                    k['user'] = i.user.username
                    k['created_at'] = i.created_at
                    task_file_json.append(k)
            return Response(task_file_json, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)


@api_view(['GET'])
def task_log_activity_view(request, form=None, pk=None):
    try:
        user = CompanyUser.objects.get(account_id=request.COOKIES['account_id'])
        if not TaskActivityLogs.objects.filter(user=user).exists():
            logs_serializer = TaskActivityLogsSerializer(
                data={'user': str(user.id), 'log_type': 'INFO',
                      'log_description': f"""{user.username} Has Started Activity"""})
            if logs_serializer.is_valid():
                logs_serializer.save()
        return Response(task_log_activity_json(TaskActivityLogs.objects.filter(user=user)), status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return Response({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=500)
