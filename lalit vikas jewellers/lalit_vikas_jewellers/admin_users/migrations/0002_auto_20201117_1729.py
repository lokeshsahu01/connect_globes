# Generated by Django 3.1.3 on 2020-11-17 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='role',
            new_name='user_role',
        ),
    ]
