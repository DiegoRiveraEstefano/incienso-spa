import base64

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Product, User
from apps.cart.models import Cart, ProductCart


def create_order(user_id, data: dict):
    cart = get_object_or_404(Cart, user=user_id)
    if not cart:
        return None

    if cart.is_empty():
        return None

    cart_products = cart.products.all()
    data['user'] = get_object_or_404(User, id=user_id)
    order = Order(**data)
    order.save()
    for i in cart_products:
        order_item = OrderItem(
            order=order,
            product=i.product,
            quantity=i.quantity
        )
        order_item.save()
    cart.set_empty()
    return order


def get_paypal_token() -> str:
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {0}".format(base64.b64encode((client_id + ":" + client_secret).encode()).decode())
    }

    token = requests.post(url, data, headers=headers)
    return token.json()['access_token']


def make_pay_order(order: Order, return_url, cancel_url):
    token = get_paypal_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    application_context = {
        "return_url": return_url,
        "cancel_url": cancel_url,
        "brand_name": "Incienso Inacap",
        "landing_page": "BILLING",
        "shipping_preference": "NO_SHIPPING",
        "user_action": "CONTINUE"
    }

    purchase_units = [
        {
            "reference_id": str(order.uuid),
            "description": "Incienso",

            "custom_id": "CUST-Incienso",
            "soft_descriptor": "Incienso",
            "amount": {
                "currency_code": "USD",
                "value": order.get_total_cost(),
            },
        }
    ]

    json_data = {
        "intent": "CAPTURE",
        'application_context': application_context,
        'purchase_units': purchase_units
    }

    response = requests.post(
        'https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=json_data)
    payment_id = response.json()['id']
    order.payment_id = payment_id
    order.save()
    payment_link = response.json()['links'][1]['href']
    return order, payment_link


def get_payment_status(order: Order):
    headers = {'Authorization': f'Bearer {get_paypal_token()}'}
    response = requests.get(
        f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order.payment_id}', headers=headers)

    data = response.json()
    approved = data['status'] == 'APPROVED'
    value = float(data['purchase_units'][0]['amount']['value']) == order.get_total_cost()

    if not approved:
        return False, {'context': 'No Aprobado'}

    if not value:
        return True, {'context': 'Cantidad Incorrecta'}

    order.paid = True
    cart = Cart.objects.get(user=order.user)
    cart.set_empty()
    for i in order.get_items():
        i.product.stock -= i.quantity
        i.product.save()
    order.save()
    return True, {'context': 'Pago Correctamente Realizado'}