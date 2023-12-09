from django_filters import rest_framework as filters
from .models import Product, ProductTag, ProductDiscount


class ProductFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains'],
            'active': ['exact', 'contains'],
            'category': ['exact', 'contains'],
            'stock': ['lte', 'gte'],
            'price': ['lte', 'gte'],
        }


class ProductDiscountFilter(filters.FilterSet):

    end_date = filters.DateRangeFilter()
    start_date = filters.DateRangeFilter()

    class Meta:
        model = ProductDiscount
        fields = {
            'code': ['exact', 'contains'],
            'type': ['exact', 'contains'],
            'product__name': ['exact', 'contains'],
            'value': ['lte', 'gte'],
        }