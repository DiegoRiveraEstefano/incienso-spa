from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Blog, BlogCategory
from .serializers import BlogReadSerializer, BlogWriteSerializer, BlogFormSerializer


class BlogViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    serializer_class = BlogReadSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Blog.objects.all()
        return Blog.objects.filter(active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response({'blogs': queryset},
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
