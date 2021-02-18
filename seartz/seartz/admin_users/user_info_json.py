from django.forms.models import model_to_dict
from .models import *


def user_json_info(obj):
    user_json = model_to_dict(obj)
    user_json.pop("password")
    user_json.pop("last_login")
    user_json.pop("groups")
    user_json.pop("user_permissions")
    if 'user_image' in user_json:
        user_json['user_image'] = obj.user_image.url if obj.user_image.name else obj.user_image.name
    if "user_role" in user_json and user_json["user_role"] != '':
        user_json["user_role"] = UserRole.objects.get(id=obj.user_role).role
    if "user_department" in user_json and user_json["user_department"] != '' and user_json["user_department"] is not None:
        user_json["user_department"] = UserDepartment.objects.get(id=obj.user_department).department
    if "sub_user" in user_json and user_json["sub_user"] != '' and user_json["sub_user"] is not None:
        user_json["sub_user"] = User.objects.get(id=obj.sub_user).username
    # user_json.pop('_id')
    return user_json
