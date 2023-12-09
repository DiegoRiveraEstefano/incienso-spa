from rest_framework import viewsets, status, exceptions
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from .filters import ProductFilter, ProductDiscountFilter
from .models import Product, ProductTag, ProductDiscount
from .serializers import ProductSerializer, ProductTagSerializer, ProductReadSerializer, \
    ProductDiscountSerializer


class ProductViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(stock__gte=1, active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response({'products': queryset},
                        template_name='views/product/product_list.html', status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        return Response(data={'product': product},
                        template_name='views/product/product_detailed.html', status=status.HTTP_200_OK)


class ProductApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = [JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductSerializer
        return ProductReadSerializer

    def get_queryset(self):
        if not self.request:
            return Product.objects.none()

        if self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(stock__gte=1, active=True)


class ProductDiscountApiViewSet(viewsets.ModelViewSet):
    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscountSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductDiscountFilter

    def get_queryset(self):
        if not self.request:
            return ProductDiscount.objects.none()

        if self.request.user.is_staff:
            return ProductDiscount.objects.all()
        return ProductDiscount.objects.filter()
