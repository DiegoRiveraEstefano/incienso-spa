from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.views import defaults
from rest_framework import viewsets, status, exceptions
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from config.exceptions import auth_exception_handler
from .models import Product, ProductTag, ProductDiscount
from .serializers import ProductSerializer, ProductTagSerialized, ProductDiscountSerialized
from ..cart.serializers import ProductCartSerializer


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
        #product = get_object_or_404(Product, pk=kwargs['pk'])
        product = self.get_object()
        return Response(data={'product': product},
                        template_name='views/product/product_detailed.html', status=status.HTTP_200_OK)

