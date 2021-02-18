# Generated by Django 3.1.5 on 2021-02-13 05:56

import categories.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=250, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('category_image', models.FileField(blank=True, null=True, upload_to=categories.models.Categories.folder_path)),
                ('alt', models.TextField(blank=True, max_length=1000, null=True)),
                ('category_description', models.TextField(blank=True, max_length=10000, null=True)),
                ('slug', models.CharField(blank=True, max_length=250, null=True)),
                ('meta_description', models.TextField(blank=True, max_length=10000, null=True)),
                ('meta_keyword', models.CharField(blank=True, max_length=250, null=True)),
                ('meta_title', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='categories.categories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
