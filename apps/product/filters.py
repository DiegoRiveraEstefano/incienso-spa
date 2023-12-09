from django_filters import rest_framework as rest_filters
from django_filters import FilterSet
from .models import Product, ProductTag, ProductDiscount


class ProductFilter(FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains'],
            'active': ['exact', 'contains'],
            'category': ['exact', 'contains'],
            'stock': ['lte', 'gte'],
            'price': ['lte', 'gte'],
        }


class ProductRestFilter(rest_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains'],
            'active': ['exact', 'contains'],
            'category': ['exact', 'contains'],
            'stock': ['lte', 'gte'],
            'price': ['lte', 'gte'],
        }


class ProductDiscountFilter(rest_filters.FilterSet):

    end_date = rest_filters.DateRangeFilter()
    start_date = rest_filters.DateRangeFilter()

    class Meta:
        model = ProductDiscount
        fields = {
            'code': ['exact', 'contains'],
            'type': ['exact', 'contains'],
            'product__name': ['exact', 'contains'],
            'value': ['lte', 'gte'],
        }