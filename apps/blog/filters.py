from django_filters import rest_framework as filters
from .models import Blog, BlogCategory


class BlogFilter(filters.FilterSet):
    publish_data = filters.DateRangeFilter()

    class Meta:
        model = Blog
        fields = {
            'title': ['exact', 'contains'],
            'active': ['exact', 'contains'],
            'user__username': ['exact', 'contains'],
            'category__category': ['exact', 'contains'],
        }