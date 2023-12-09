from django.shortcuts import redirect, get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters import rest_framework as filters

from .filters import BlogFilter, BlogRestFilter
from .models import Blog, BlogCategory
from .serializers import BlogReadSerializer, BlogWriteSerializer, BlogFormSerializer
from ..user.models import User


class BlogViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    serializer_class = BlogReadSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BlogFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return Blog.objects.all()
        return Blog.objects.filter(active=True)

    def list(self, request, *args, **kwargs):
        filter_set = self.filterset_class(request.query_params, queryset=self.get_queryset())
        return Response({'filter': filter_set},
                        template_name='views/blog/blog_list.html', status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()
        return Response(data={'blog': blog},
                        template_name='views/blog/blog_detailed.html', status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_name='create-form')
    def get_blog_create_form(self, request):
        serializer = BlogFormSerializer()
        return Response(data={'serializer': serializer, 'categoires': BlogCategory.objects.all()},
                        template_name='views/blog/blog_create_form.html', status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        data = {
            'title': request.data['title'],
            'text': request.data['text'],
            'category': request.data['category'], #get_object_or_404(BlogCategory, pk=request.data['category']),
            'user': request.user.id,
            'image': request.data['image'].open(),
        }
        serializer: BlogWriteSerializer = BlogWriteSerializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            print(serializer.errors)
            return redirect('blog-create-form')

        blog = serializer.save()
        return Response({'blog': blog},
                        template_name='views/blog/blog_detailed.html', status=status.HTTP_200_OK)


class BlogApiViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [JSONRenderer, ]
    parser_classes = (MultiPartParser, JSONParser)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BlogRestFilter
    pagination_class = PageNumberPagination
    page_size = 10

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BlogReadSerializer
        return BlogWriteSerializer

    def get_queryset(self):
        if not self.request:
            return Blog.objects.none()

        if self.request.user.is_staff:
            return Blog.objects.all()

        return Blog.objects.filter(active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
