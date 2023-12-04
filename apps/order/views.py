from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import Cart
from apps.user.models import User
from .models import Order, OrderItem
from .logics import create_order
from .serializers import OrderSerializer, OrderItemSerializer, OrderWriteSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        order = get_object_or_404(Order, uuid=kwargs["pk"])
        products = order.get_items()
        return Response(data={
            'order': order,
            'products': products
        },
            template_name='views/order/order_details.html',
            status=status.HTTP_200_OK
        )

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(
            {'orders': queryset},
            template_name='views/order/order_list.html', status=status.HTTP_200_OK
        )

    def create(self, request: Request, *args, **kwargs):
        data = {
            'address': request.data['address'],
            'postal_code': request.data['postal_code'],
            'city': request.data['city'],
            'discount_code': request.data['discount_code']
        }
        cart = get_object_or_404(Cart, user=request.user.id)

        if cart.is_empty():
            return redirect('cart-list')

        cart_products = cart.products.all()
        data['user'] = get_object_or_404(User, id=request.user.id).id

        serialized_order = self.serializer_class(data=data)
        if not serialized_order.is_valid(raise_exception=False):
            return redirect('cart-list')

        order = serialized_order.save()
        order.save()
        for i in cart_products:
            order_item = OrderItem(
                order=order,
                product=i.product,
                quantity=i.quantity
            )
            order_item.save()
        order.total_cost = order.get_total_cost()
        order.save()
        cart.set_empty()
        return redirect('order-detail', pk=order.uuid)

    @action(methods=['GET'], detail=False, url_name='create-form')
    def get_order_create_form(self, request: Request):
        serializer = OrderWriteSerializer()
        return Response(
            {'serializer': serializer},
            status=status.HTTP_200_OK,
            template_name='views/order/order_create.html'
        )
