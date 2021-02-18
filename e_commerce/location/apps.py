from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig


class LocationConfig(AppConfig):
    name = 'location'


def create_test_user(sender, **kwargs):

    if not isinstance(sender, AuthConfig):
        return
    from .models import Country
    try:
        Country.objects.get(country_name="India")
    except Country.DoesNotExist:
        Country(country_name="India", country_code='IN', country_currency='INR', country_phone_code='+91').save()


class LocationAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_test_user)
