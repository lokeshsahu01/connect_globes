# Generated by Django 3.1.5 on 2021-02-11 10:03

from django.db import migrations, models
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=250)),
                ('product_id', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CouponCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coupon_code', models.CharField(max_length=250)),
                ('coupon_discount_amount', models.FloatField(default=0)),
                ('coupon_discount_percentage', models.FloatField(default=0)),
                ('coupon_image', models.FileField(upload_to=order.models.CouponCode.folder_path)),
                ('is_valid', models.BooleanField(default=True)),
                ('coupon_description', models.TextField(blank=True, max_length=20000, null=True)),
                ('valid_for', models.TextField(blank=True, max_length=20000, null=True)),
                ('valid_for_amount', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('user_id', models.CharField(max_length=250)),
                ('product', order.models.LIstField()),
                ('order_address_id', models.CharField(max_length=250)),
                ('order_id', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('coupon_code_id', models.CharField(max_length=250)),
                ('coupon_discount', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('status', models.CharField(max_length=250)),
                ('delivery_charge', models.IntegerField()),
                ('delivery_status', models.CharField(blank=True, max_length=250, null=True)),
                ('payment_method', models.CharField(max_length=20)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=250, null=True)),
                ('payment_status', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=250)),
                ('full_name', models.CharField(max_length=250)),
                ('mobile_number', models.CharField(max_length=250)),
                ('pin_code', models.IntegerField()),
                ('address', models.TextField(max_length=20000)),
                ('landmark', models.CharField(blank=True, max_length=250, null=True)),
                ('town_city', models.CharField(max_length=250)),
                ('State', models.CharField(max_length=250)),
                ('address_type', models.CharField(max_length=250)),
                ('is_default', models.BooleanField(default=False)),
                ('is_select', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]