from django.forms.models import model_to_dict


def user_json_info(obj):
    user_json = model_to_dict(obj)
    user_json.pop("password")
    user_json.pop("last_login")
    user_json.pop("groups")
    user_json.pop("user_permissions")
    if "user_role" in user_json and user_json["user_role"] is not None:
        user_json["user_role"] = obj.user_role.role
    if "user_department" in user_json and user_json["user_department"] is not None:
        user_json["user_department"] = obj.user_department.department
    if "sub_user" in user_json and user_json["sub_user"] is not None:
        user_json["sub_user"] = obj.sub_user.username
    return user_json
