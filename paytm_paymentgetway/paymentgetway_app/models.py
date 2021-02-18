from django.db import models


class OnlineOrder(models.Model):
    email = models.EmailField(max_length=250, unique=True)
    order_id = models.CharField(max_length=250, unique=True)
    amount = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)


class PaytmResponseModel(models.Model):
    paytm_response = models.TextField(max_length=65500, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
