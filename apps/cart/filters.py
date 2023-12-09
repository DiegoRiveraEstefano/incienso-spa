from django_filters import rest_framework as filters
from .models import Cart, ProductCart


class CartFilter(filters.FilterSet):

    class Meta:
        model = Cart
        fields = {
            'user__username': ['exact', 'contains'],
        }


class CartProductFilter(filters.FilterSet):

    class Meta:
        model = ProductCart
        fields = {
            'cart__uuid': ['exact', 'contains'],
            'product__name': ['exact', 'contains'],
            'quantity': ['gte', 'lte'],
        }