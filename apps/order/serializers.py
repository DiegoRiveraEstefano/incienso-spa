from rest_framework import serializers
from .models import Order, OrderItem
from apps.product.serializers import ProductSerializer


class OrderWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['address', 'postal_code', 'city']

class OrderSerializer(serializers.ModelSerializer):
    total_cost = serializers.IntegerField(source='get_total_cost', read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'address', 'postal_code', 'city', 'created', 'updated', 'paid', 'id', 'total_cost']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']