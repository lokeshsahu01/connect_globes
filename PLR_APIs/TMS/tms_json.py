from django.forms.models import model_to_dict


def task_in_json(obj):
    task_list = []
    for i in obj:
        j = model_to_dict(i)
        # j['user'] = i.user.username
        # if "assigned_to_user" in j and i.assigned_to_user is not None:
        #     j['assigned_to_user'] = i.assigned_to_user.username
        # if 'assigned_to_group' in j and i.assigned_to_group is not  None:
        #     j['assigned_to_group'] = i.assigned_to_group.group_name
        # if 'user_department' in j and i.user_department is not None:
        #     j['user_department'] = i.user_department.department_name
        j['created_at'] = i.created_at
        task_list.append(j)
    return task_list


def single_task_json(i):
    j = model_to_dict(i)
    # j['user'] = i.user.username
    # if "assigned_to_user" in j and i.assigned_to_user is not None:
    #     j['assigned_to_user'] = i.assigned_to_user.username
    # if 'assigned_to_group' in j and i.assigned_to_group is not None:
    #     j['assigned_to_group'] = i.assigned_to_group.group_name
    # if 'user_department' in j and i.user_department is not None:
    #     j['user_department'] = i.user_department.department_name
    j['created_at'] = i.created_at
    return j


def task_log_activity_json(obj):
    task_list = []
    for i in obj:
        j = model_to_dict(i)
        j['created_at'] = i.created_at
        task_list.append(j)
    return task_list