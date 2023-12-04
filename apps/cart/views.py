from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import ProductCart, Cart, Product
from .serializers import ProductCartSerializer, CartSerializer, ProductCartReadSerializer
from .logics import add_product, remove_product, get_cart


class CartViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    permission_classes = [AllowAny, IsAuthenticated]
    serializer_class = CartSerializer
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser, ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        cart: Cart = get_cart(request.user.id)
        return Response(data={'cart': cart},
                        template_name='views/product/product_detailed.html', status=status.HTTP_200_OK)

    #def retrieve(self, request, *args, **kwargs):
    #    return redirect('cart-list')

    def create(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        product_cart = add_product(request.user.id, data['product_uuid'])
        return Response(
            data={'product': product_cart},
            template_name='components/cart/cart_add_product.html',
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=True, url_name='add-product')
    def add_product(self, request: Request):
        data = request.data
        product_cart = add_product(request.user.id, data['product_uuid'])
        return Response(
            data={'product': product_cart},
            template_name='components/cart/cart_add_product.html',
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'], detail=False, url_name='remove-product')
    def remove_product(self, request: Request, *args, **kwargs):
        data = request.data
        remove_product(request.user.id, data['product_id'])
        return Response(
            template_name='components/cart/cart_remove_product.html',
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated], url_name='clear-cart')
    def clear_cart(self, request: Request, *args, **kwargs):
        cart: Cart = get_cart(request.user.id)
        cart.set_empty()
        return redirect('cart-detail')        