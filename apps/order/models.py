from uuid import uuid4
from django.db import models
from apps.product.models import Product
from apps.user.models import User
from datetime import datetime


class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    discount_code = models.CharField(max_length=16, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=128, blank=True)
    total_cost = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order(id={self.uuid}, user={self.user}, created={self.created})"

    def discount_is_valid(self):
        try:
            return self.created.strftime('%Y-%m-%d') == datetime.strptime(self.discount_code, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            return False

    def get_items(self):
        return self.items.all()

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount_is_valid():
            return int(total * 0.8)
        return total

    def get_raw_total_cost(self):
        return sum(item.get_raw_cost() for item in self.items.all())

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
        return self.product.get_final_price() * self.quantity

    def get_raw_cost(self):
        return self.product.price * self.quantity