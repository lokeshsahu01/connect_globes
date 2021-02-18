from .models import *


def user_in_json(s1: dict, s2: dict):
    s1, s2 = list(s1), list(s2)
    d = []
    if len(s1) == len(s2):
        for i in range(len(s1)):
            k = dict(s1[i])
            p = dict(s2[i])
            k.update(p)
            k.pop('password')
            d.append(k)
    return d


def child_tree_users(parent_user):
    if parent_user.is_company:
        return list(CompanyUser.objects.filter(company_sub_user_id=parent_user))

    def child_tree_user(parent_user, sub_c_user):
        if CompanySubUser.objects.filter(user_in_under=parent_user).exists():
            child_user = CompanySubUser.objects.filter(user_in_under=parent_user)
            for k in child_user:
                sub_c_user.append(k.user)
                child_tree_user(k.user, sub_c_user)
            return sub_c_user
    return child_tree_user(parent_user, [])


def parent_tree_users(parent_user):
    if parent_user.is_company:
        return []

    def child_tree_user(parent_user, sub_c_user):
        if CompanySubUser.objects.filter(user=parent_user).exists():
            child_user = CompanySubUser.objects.filter(user=parent_user)
            for k in child_user:
                sub_c_user.append(k.user_in_under)
                child_tree_user(k.user_in_under, sub_c_user)
            return sub_c_user

    return child_tree_user(parent_user, [])
