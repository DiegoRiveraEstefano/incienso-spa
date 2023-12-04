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