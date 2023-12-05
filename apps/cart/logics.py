from django.shortcuts import get_object_or_404
from .models import ProductCart, Product, Cart


def get_cart(user_id):
    return get_object_or_404(Cart, user=user_id)


def add_product(user_id, product_id, quanty: int = 1):
    cart = get_cart(user_id)
    product = get_object_or_404(Product, pk=product_id)
    if not product or not cart:
        return None

    products = ProductCart.objects.filter(cart=cart, product=product)

    if len(products) == 0:
        product_cart = ProductCart(cart=cart, product=product, quantity=quanty)
    else:
        product_cart = products[0]
        product_cart.quantity = product_cart.quantity + quanty

    product_cart.save()
    return product_cart


def remove_product(user_id, product_id):
    cart = get_cart(user_id)
    product = get_object_or_404(Product, pk=product_id)
    if not product or not cart:
        return None

    products = ProductCart.objects.filter(cart=cart, product=product)
    if len(products) == 0:
        return None

    product_cart = products[0]
    product_cart.delete()