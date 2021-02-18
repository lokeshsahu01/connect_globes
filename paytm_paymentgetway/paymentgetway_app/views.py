from django.shortcuts import render
from rest_framework.decorators import api_view
# from .serializers import *
from django.conf import settings
from .Checksum import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *


@api_view(['GET', 'POST'])
def paytm_checksum_gen_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        param_dict = {
            'MID': settings.PAYTM_MERCHANT_ID,
            'ORDER_ID': str(order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8888/api/v1/paytm/handle_request/',
        }
        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, settings.PAYTM_MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
    return render(request, 'paytm_gen.html')


@csrf_exempt
def paytm_checksum_handle_request_view(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    checksum = None
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict, settings.PAYTM_MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            PaytmResponseModel(paytm_response=str(response_dict)).save()
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paytm_gen.html', {'response': response_dict})


@api_view(['GET', 'POST'])
def paytm_refund_checksum_view(request):
    pass
