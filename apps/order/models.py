from uuid import uuid4
from django.db import models
from apps.product.models import Product
from apps.user.models import User


class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order(id={self.uuid}, user={self.user}, created={self.created})"

    def get_items(self):
        return self.items.all()

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_payment_items(self):
        return ""


class OrderItem(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", 'quantity']
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def __str__(self):
        return f"OrderItem(id={self.uuid}, product={self.product}, quantity={self.quantity})"

    def get_cost(self):
        return self.product.price * self.quantity