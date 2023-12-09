from django_filters import rest_framework as rest_filters
from django_filters import FilterSet, filters
from .models import Blog, BlogCategory


class BlogFilter(FilterSet):
    publish_data = filters.DateRangeFilter()

    class Meta:
        model = Blog
        fields = {
            'title': ['exact', 'contains'],
            'active': ['exact', 'contains'],
            'user__username': ['exact', 'contains'],
            'category__category': ['exact', 'contains'],
        }


class BlogRestFilter(rest_filters.FilterSet):
    publish_data = rest_filters.DateRangeFilter()

    class Meta:
        model = Blog
        fields = {
            'title': ['exact', 'contains'],
            'active': ['exact', 'contains'],
            'user__username': ['exact', 'contains'],
            'category__category': ['exact', 'contains'],
        }