from django_filters import rest_framework as filters
from .models import Order, OrderItem


class OrderFilter(filters.FilterSet):
    created = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Order
        fields = {
            'user__username': ['exact', 'contains'],
            'address': ['exact', 'contains'],
            'postal_code': ['exact', 'contains'],
            'city': ['exact', 'contains'],
            'discount_code': ['exact', 'contains'],
            'payment_id': ['exact', 'contains'],
            'total_cost': ['gte', 'lte'],
        }


class OrderItemFilter(filters.FilterSet):

    class Meta:
        model = OrderItem
        fields = {
            'uuid': ['exact', 'contains'],
            'order__uuid': ['exact', 'contains'],
            'product__name': ['exact', 'contains'],
            'quantity': ['gte', 'lte'],
        }