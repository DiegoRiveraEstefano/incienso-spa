from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Product, ProductTag, ProductDiscount


class ProductSerializer(serializers.ModelSerializer):

    discounts = serializers.SerializerMethodField(read_only=True)
    final_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)

    def get_image(self, obj):
        return obj.image.url if obj.image else settings.STATIC_URL + 'images/product/default_image.png'

    def get_thumbnail(self, obj):
        return obj.thumbnail.url if obj.thumbnail else settings.STATIC_URL + 'images/product/default_thumbnail.png'

    def get_discounts(self, obj):
        return obj.get_discounts()

    def get_final_price(self, obj):
        return obj.final_price

    class Meta:

        model = Product
        depth = 1
        fields = [
            'uuid', 'name', 'stock', 'active', 'price', 'price',
            'description', 'thumbnail', 'image', 'category',
            'discounts', 'final_price'
        ]


class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'stock', 'active', 'price', 'price',
            'description', 'thumbnail', 'image', 'category',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=['name', 'description']
            ),
        ]


class ProductDiscountSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductDiscount
        depth = 1
        fields = [
            'uuid', 'code', 'start_date', 'end_date',
            'type', 'value', 'product'
        ]


class ProductTagSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductTag
        depth = 1
        fields = [
            'uuid', 'tag', 'active', 'product'
        ]
