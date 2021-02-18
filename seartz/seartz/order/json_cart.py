from django.forms.models import model_to_dict
from product.models import Product
from product.product_json import *


def cart_json(obj):
    k = model_to_dict(obj)
    return k


def carts_json(obj):
    cart_list = []
    total_price = 0
    total_selling_price = 0
    discount = 0
    delivery_charge = 0
    quantity = 0
    for i in obj:
        k = model_to_dict(i)
        product = one_product_json(Product.objects.get(id=i.product_id))
        total_selling_price += i.quantity * product['selling_price'] if product['selling_price'] else i.quantity * product['price']
        total_price += i.quantity * product['price']
        discount += i.quantity * (product['price'] - product['selling_price']) if product['selling_price'] else 0
        quantity += i.quantity
        if product['delivery_charge']:
            delivery_charge += product['delivery_charge']
        k['product_id'] = product
        cart_list.append(k)
    return cart_list, total_price, total_selling_price, discount, delivery_charge, quantity


def order_address_json(obj):
    order_address_list = []
    for i in obj:
        k = model_to_dict(i)
        order_address_list.append(k)
    return order_address_list


def order_json(obj):
    order_list = []
    for i in obj:
        k = model_to_dict(i)
        order_list.append(k)
    return order_list
