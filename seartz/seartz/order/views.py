from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from rest_framework.response import Response
from .json_cart import *
from datetime import datetime, timedelta
from django.shortcuts import render
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from random import randint
from seartz.mongoDBConnection import *


@api_view(['POST', ])
@decorator_from_middleware(CreateCartMiddleware)
def create_cart_view(request, form=None):
    try:
        product = Product.objects.get(id=form.cleaned_data['product'])
        if Cart.objects.filter(user_id=request.user.id, product_id=product.id).exists():
            cart_obj = Cart.objects.get(user_id=request.user.id, product_id=product.id)
            if form.cleaned_data['quantity'] == 0:
                cart_obj.delete()
                return Response({'data': None, 'message': 'Successfully deleted cart', 'status': 200}, status=200)
            cart_obj.quantity = form.cleaned_data['quantity']
            cart_obj.total_price = product.selling_price * form.cleaned_data['quantity'] if product.selling_price else product.price * form.cleaned_data['quantity']
            cart_obj.updated_at = datetime.now()
            cart_obj.save()
            cart = cart_json(Cart.objects.get(user_id=request.user.id, product_id=product.id))
        else:
            Cart(user_id=request.user.id, product_id=product.id, quantity=form.cleaned_data['quantity'],
                 total_price=product.selling_price * form.cleaned_data['quantity'] if product.selling_price else product.price * form.cleaned_data['quantity']).save()
            cart = cart_json(Cart.objects.last())
        return Response({'data': cart, 'message': 'Successfully created cart', 'status': 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['PUT', ])
@decorator_from_middleware(CreateCartMiddleware)
def edit_cart_view(request, form=None, pk=None):
    if Cart.objects.filter(id=pk).exists():
        cart_obj = Cart.objects.get(id=pk)
        product = Product.objects.get(id=cart_obj.product_id)
        if form.cleaned_data['quantity'] == 0:
            cart_obj.delete()
            return Response({'data': None, 'message': 'Successfully deleted cart', 'status': 200}, status=200)
        else:
            cart_obj.quantity = form.cleaned_data['quantity']
            cart_obj.updated_at = datetime.now()
            cart_obj.total_price = product.selling_price * form.cleaned_data['quantity'] if product.selling_price else product.price * form.cleaned_data['quantity']
            cart_obj.save()
            cart = cart_json(Cart.objects.get(id=pk))
        return Response({'data': cart, 'message': f'successfully Update Cart {pk}', 'status': 200}, status=200)
    else:
        return Response({'data': None, 'message': 'Cart Is Empty', 'status': 200}, status=200)


@api_view(['DELETE', ])
def delete_cart_view(request, pk=None):
    if Cart.objects.filter(id=pk).exists():
        cort_obj = Cart.objects.get(id=pk)
        cort_obj.delete()
        return Response({'data': None, 'message': 'Successfully deleted cart', 'status': 200}, status=200)
    else:
        return Response({'data': None, 'message': 'Cart Is Empty', 'status': 200}, status=200)


@api_view(['GET', ])
def get_cart_view(request, pk=None):
    if pk:
        if Cart.objects.filter(id=pk).exists():
            cart = cart_json(Cart.objects.get(id=pk))
            return Response({'data': cart, 'message': 'Successfully Get cart', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Cart Is Empty', 'status': 200}, status=200)
    else:
        if Cart.objects.filter(user_id=request.user.id).exists():
            cart, total_price, total_selling_price, discount, delivery_charge, quantity = carts_json(Cart.objects.filter(user_id=request.user.id))
            return Response({'data': cart, 'total_price': total_price, 'total_selling_price': total_selling_price, 'discount': discount, 'delivery_charge': delivery_charge, 'quantity': quantity,
                             'message': 'Successfully Get cart', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Cart Is Empty', 'status': 200}, status=200)


@api_view(['DELETE', ])
def delete_all_view(request):
    if Cart.objects.filter(user=request.user.id).exists():
        Cart.objects.filter(user=request.user.id).delete()
        return Response({'data': None, 'message': 'Successfully deleted cart', 'status': 200}, status=200)
    else:
        return Response({'data': None, 'message': 'Cart Is Empty', 'status': 200}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(CreateOrderAddressMiddleware)
def create_order_address_view(request, form=None, pk=None):
    try:
        form.cleaned_data['user_id'] = request.user.id
        OrderAddress(**form.cleaned_data).save()
        order_address_obj = order_address_json(OrderAddress.objects.filter(user_id=request.user.id))
        return Response({'data': order_address_obj, 'message': 'Successfully Save Order Address', 'status': 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['PUT', ])
@decorator_from_middleware(CreateOrderAddressMiddleware)
def edit_order_address_view(request, form=None, pk=None):
    try:
        if pk and OrderAddress.objects.filter(id=pk).exists():
            order_address_obj = OrderAddress.objects.get(id=pk)
            order_address_obj.full_name = form.cleaned_data['full_name']
            order_address_obj.mobile_number = form.cleaned_data['mobile_number']
            order_address_obj.pin_code = form.cleaned_data['pin_code']
            order_address_obj.address = form.cleaned_data['address']
            order_address_obj.landmark = form.cleaned_data['landmark']
            order_address_obj.town_city = form.cleaned_data['town_city']
            order_address_obj.State = form.cleaned_data['State']
            order_address_obj.address_type = form.cleaned_data['address_type']
            order_address_obj.is_default = form.cleaned_data['is_default']
            order_address_obj.updated_at = datetime.now()
            order_address_obj.save()
            order_address_obj = model_to_dict(OrderAddress.objects.get(id=pk))
            return Response({'data': order_address_obj, 'message': 'Successfully Save Order Address', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Delivery Address Not Found', 'status': 404}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['PUT', ])
def edit_order_address_view(request, pk=None):
    try:
        if pk and OrderAddress.objects.filter(id=pk).exists():
            OrderAddress.objects.filter(user_id=OrderAddress.objects.get(id=pk).user_id).update(is_select=False)
            order_address_obj = OrderAddress.objects.get(id=pk)
            order_address_obj.is_select = True
            order_address_obj.save()
            order_address_obj = model_to_dict(OrderAddress.objects.get(id=pk))
            return Response({'data': order_address_obj, 'message': 'Successfully Save Order Address', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Delivery Address Not Found', 'status': 404}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['GET', ])
def get_order_address_view(request, pk=None):
    try:
        if pk:
            if OrderAddress.objects.filter(id=pk).exists():
                order_address_obj = model_to_dict(OrderAddress.objects.get(id=pk))
                return Response({'data': order_address_obj, 'message': 'Successfully Get Order Address', 'status': 200}, status=200)
            else:
                return Response({'data': None, 'message': 'Delivery Address Not Found', 'status': 200}, status=200)
        else:
            if OrderAddress.objects.filter(user_id=request.user.id).exists():
                order_address_obj = order_address_json(OrderAddress.objects.filter(user_id=request.user.id))
                return Response({'data': order_address_obj, 'message': 'Successfully Get Order Address', 'status': 200}, status=200)
            else:
                return Response({'data': None, 'message': 'Delivery Address Not Found', 'status': 200}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


def create_rozor_payment_view(request, form=None, pk=None):
    client = razorpay.Client(auth=("rzp_test_Agfb7ibNceP6Su", "jId4O4vlgv4TR9V08bJF7pJJ"))
    payment = client.order.create({'amount': 5000, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, 'index.html')


@csrf_exempt
def success(request):
    print(request.POST)
    return render(request, "success.html")


@api_view(['POST', ])
@decorator_from_middleware(CreateOrderMiddleware)
def create_order_view(request, form=None, pk=None):
    try:
        if Cart.objects.filter(user_id=request.user.id).exists():
            cart_obj = Cart.objects.filter(user_id=request.user.id)
            order_address_obj = OrderAddress.objects.get(id=form.cleaned_data['order_address_id'])
            coupon_code_obj = None
            if 'coupon_code' in form.cleaned_data and form.cleaned_data['coupon_code'] and CouponCode.objects.get(coupon_code=form.cleaned_data['coupon_code']).is_valid:
                coupon_code_obj = CouponCode.objects.get(coupon_code=form.cleaned_data['coupon_code'])
            rend_id = None
            for i in range(10):
                rend_id = randint(10 ** (8 - 1), (10 ** 8) - 1)
                if not Order.objects.filter(order_id=rend_id).exists():
                    break
            if form.cleaned_data['payment_method'] == 'Cash On Delivery':
                payment_method = 'Cash On Delivery'
                razorpay_payment_id = None
                payment_status = 'Unpaid'
            elif form.cleaned_data['payment_method'] == 'Razorpay':
                payment_method = 'Razorpay'
                razorpay_payment_id = form.cleaned_data['razorpay_payment_id']
                payment_status = 'Paid'
            else:
                return Response({'data': None, 'message': 'Payment Method not valid', 'status': 404}, status=200)
            total_price, quantity, delivery_charge = 0, 0, 0
            products = []
            for i in cart_obj:
                product_obj = Product.objects.get(id=i.product_id)
                total_price += i.total_price
                quantity += i.quantity
                if product_obj.delivery_charge:
                    delivery_charge += product_obj.delivery_charge
                products.append({'product_id': product_obj.id, 'seller_id': product_obj.user_id, 'quantity': i.quantity, 'total_price': i.total_price,
                                 'delivery_charge': product_obj.delivery_charge, 'shipping_address': '', 'status': 'Complete', 'delivery_time': product_obj.delivery_time})
                i.delete()
            if coupon_code_obj:
                coupon_discount_amount = (total_price * coupon_code_obj.coupon_discount_percentage)/100
                if coupon_discount_amount > coupon_code_obj.coupon_discount_amount:
                    coupon_discount_amount = coupon_code_obj.coupon_discount_amount
                total_discounted_price = total_price - coupon_discount_amount
                coupon_code_id = coupon_code_obj.id
                coupon_discount = coupon_discount_amount
            else:
                total_discounted_price = total_price
                coupon_code_id = None
                coupon_discount = 0
            datetime_5 = datetime.now() + timedelta(days=5)
            date = datetime_5.strftime("%B") + ' ' + datetime_5.strftime("%d")
            order_data = {'user_id': request.user.id, 'product': products, 'order_address_id': order_address_obj.id,
                          'order_id': rend_id, 'quantity': quantity, 'price': total_price,
                          'coupon_code_id': coupon_code_id, 'coupon_discount': coupon_discount,
                          'total_price': total_discounted_price, 'status': 'Order Placed', 'delivery_charge': delivery_charge, "delivery_status": f'Delivery expected by {date}',
                          'payment_method': payment_method, 'razorpay_payment_id': razorpay_payment_id, 'payment_status': payment_status,
                          }
            Order(**order_data).save()
            order_obj = model_to_dict(Order.objects.last())
            return Response({'data': order_obj, 'message': 'Successfully Get Order Address', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'User`s Cart is Empty', 'status': 404}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({'data': None, 'message': f"{e}, {f_name}, {exc_tb.tb_lineno}", 'status': 500}, status=200)


@api_view(['PUT', ])
def cancel_order_view(request, order_id=None, product_id=None):
    order_model = database['order_order']
    edit_order_obj = order_model.update({"order_id": order_id, "product.product_id": product_id}, {'$set': {"product.$.status": "Cancelled"}})
    order_obj = order_model.find({"order_id": order_id, "product.product_id": product_id})
    data = []
    for k in order_obj:
        k.pop('_id')
        data.append(k)
    return Response({'data': data, 'message': 'Order Not Found', 'status': 404}, status=200)


@api_view(['GET', ])
def get_order_view(request, pk=None):
    if pk:
        if Order.objects.filter(order_id=pk).exists():
            return Response({'data': model_to_dict(Order.objects.get(order_id=pk)), 'message': 'Successfully Get Order', 'status': 200}, status=200)
        else:
            return Response({'data': None, 'message': 'Order Not Found', 'status': 404}, status=200)
    else:
        order_obj = order_json(Order.objects.filter(user_id=request.user.id))
        return Response({'data': order_obj, 'message': 'Successfully Get Order', 'status': 200}, status=200)
