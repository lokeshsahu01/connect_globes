# Generated by Django 3.0.5 on 2020-12-09 06:38

import CompanyUser.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=250)),
                ('is_login', models.BooleanField(default=False)),
                ('last_login', models.DateField(blank=True, null=True)),
                ('username', models.CharField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('is_company', models.BooleanField(default=False)),
                ('key', models.CharField(blank=True, max_length=250, null=True)),
                ('account_id', models.IntegerField(default=45387239, unique=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('company_sub_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_sub_user', to='CompanyUser.CompanyUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to='CompanyUser.CompanyUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='CompanyUser.CompanyUser')),
            ],
        ),
        migrations.CreateModel(
            name='CompanySubUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=255, unique=True)),
                ('phone', models.CharField(default='', max_length=100)),
                ('mobile', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('location', models.TextField(default='', max_length=1000)),
                ('user_image', models.FileField(default='', upload_to=CompanyUser.models.CompanySubUser.folder_path)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('is_deactivate', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('T', 'Live'), ('F', 'Not live')], default='T', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_id', to='CompanyUser.CompanyUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='CompanyUser.CompanyUser')),
                ('user_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CompanyUser.UserDepartment')),
                ('user_in_under', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_in_under', to='CompanyUser.CompanyUser')),
                ('user_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CompanyUser.UserLevels')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise_id', models.CharField(max_length=200, verbose_name='Enterprise ID')),
                ('company_name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('company_address', models.TextField(max_length=500, verbose_name='Company Address')),
                ('company_contact', models.CharField(max_length=200, verbose_name='Company Contact')),
                ('company_pan', models.CharField(max_length=255, verbose_name='Company PAN')),
                ('company_gstn', models.CharField(blank=True, max_length=255, verbose_name='Company GSTN')),
                ('owner_name', models.CharField(default='', max_length=255, verbose_name='Company Primary admin Name')),
                ('company_primary_email', models.EmailField(default='', max_length=255, unique=True, verbose_name='Company Primary Email- ID')),
                ('company_primary_mobile', models.CharField(default='', max_length=200, unique=True, verbose_name='Company Primary Mobile')),
                ('allowed_user', models.IntegerField(default=0, verbose_name='No. of users required')),
                ('allowed_space', models.IntegerField(choices=[(5, '5 GB'), (10, '10 GB'), (15, '15 GB'), (20, '20 GB')], default=0, verbose_name='Space required')),
                ('company_image', models.FileField(default='', upload_to=CompanyUser.models.CompanyDetails.folder_path)),
                ('allow_scanning', models.CharField(choices=[('t', 'Yes'), ('f', 'No')], default='f', max_length=2, verbose_name='Scanning required')),
                ('estimate_page', models.IntegerField(default=0, verbose_name='Estimated pages')),
                ('status', models.BooleanField(default=True)),
                ('subscription', models.CharField(choices=[('DMS', 'DMS'), ('TMS', 'TMS'), ('BOTH', 'BOTH')], max_length=8)),
                ('subscription_duration', models.CharField(choices=[('0', 'Free trial'), ('1', 'year'), ('2', 'years')], max_length=8)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='CompanyUser.CompanyUser', verbose_name='Company Primary User Name')),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
