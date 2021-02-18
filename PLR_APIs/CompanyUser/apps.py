from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig


class CompanyuserConfig(AppConfig):
    name = 'CompanyUser'


def create_test_user(sender, **kwargs):
    if not settings.DEBUG:
        return
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    User = get_user_model()
    manager = User.objects
    try:
        manager.get(username="admin")
    except User.DoesNotExist:
        manager.create_superuser(username='admin', email='admin@plr.com', is_superuser=True, is_staff=True,
                                 is_active=True, password='12345678')


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_test_user)