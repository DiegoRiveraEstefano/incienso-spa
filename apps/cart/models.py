from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user.models import User
from apps.product.models import Product


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        ordering = ('user',)
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart(id={self.id}, user={self.user})"

    def get_products(self):
        return self.products.all()

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.products.all())

    def is_empty(self):
        return True if len(self.products.all()) == 0 else False

    def set_empty(self):
        for i in self.products.all():
            i.delete()


class ProductCart(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('cart', 'product')
        verbose_name = 'ProductCart'
        verbose_name_plural = 'ProductCarts'

    def __str__(self):
        return f"ProductCart(id={self.id}, cart={self.cart}, product={self.product}, quantity={self.quantity})"

    def get_cost(self):
        return self.product.price * self.quantity


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_cart(sender, instance=None, created=False, **kwargs):
    if created:
        Cart.objects.create(user=instance)