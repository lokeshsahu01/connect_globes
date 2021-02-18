from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint


class AdminUsersConfig(AppConfig):
    name = 'admin_users'


def create_test_user(sender, **kwargs):

    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    from .models import UserRole, UserDepartment
    try:
        UserRole.objects.get(role="Admin")
    except UserRole.DoesNotExist:
        UserRole(role="Admin", is_create_user=True).save()
        UserRole(role="Buyer", is_create_user=False).save()
        UserRole(role="Artist", is_create_user=False).save()
    try:
        UserDepartment.objects.get(department="Admin")
    except UserDepartment.DoesNotExist:
        UserDepartment(department="Admin").save()
    user = get_user_model()
    manager = user.objects
    try:
        manager.get(mobile="9087654321")
    except user.DoesNotExist:
        manager.create_superuser(email='Admin@lvjewellers.com', mobile='9087654321',
                                 first_name='Admin', last_name='Admin',
                                 account_id=randint(10**(8-1), (10**8)-1), is_superuser=True, is_staff=True,
                                 is_active=True, user_role=UserRole.objects.get(role="Admin").id,
                                 user_department=UserDepartment.objects.get(department="Admin").id,
                                 password='asdf')


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_test_user)
