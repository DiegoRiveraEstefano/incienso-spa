from rest_framework import serializers
from .models import Order, OrderItem
from apps.product.serializers import ProductSerializer


class OrderWriteSerializer(serializers.ModelSerializer):

    address = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    postal_code = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    city = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    discount_code = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    class Meta:
        model = Order
        fields = ['address', 'postal_code', 'city', 'discount_code']


class OrderSerializer(serializers.ModelSerializer):
    total_cost = serializers.IntegerField(source='get_total_cost', read_only=True)
    raw_total_cost = serializers.IntegerField(source='get_raw_total_cost', read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'address', 'postal_code',
                  'city', 'uuid', 'total_cost', 'discount_code', 'raw_total_cost', 'created', 'updated']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderPaymentSerializer(serializers.Serializer):
    link = serializers.URLField(max_length=2048)