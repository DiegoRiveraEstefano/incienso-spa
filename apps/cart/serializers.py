from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from .models import Cart, ProductCart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user']


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = ['product', 'quantity']


class ProductCartReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True)

    class Meta:
        model = ProductCart
        fields = ['product', 'quantity']
        depth = 1
