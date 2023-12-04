from uuid import uuid4

from django.db import models
from django.utils import timezone


class Product(models.Model):

    CATEGORIES = [
        ('SINGLE', 'unico'),
        ('PACK', 'pack'),
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=64, null=False, unique=True)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    description = models.TextField(max_length=256, blank=True)
    thumbnail = models.ImageField(blank=True)
    image = models.ImageField(blank=True)
    category = models.CharField(choices=CATEGORIES, default='SINGLE', max_length=32)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"Product(id={self.uuid}, name={self.name}, category={self.category})"

    @property
    def final_price(self):
        base_price = self.price
        for i in self.get_discounts():

            discount: ProductDiscount = i
            if not discount.active:
                continue

            if discount.type == 'FIXED':
                base_price -= discount.value
            elif discount.type == 'PERCENTAGE':
                base_price -= int(base_price * (discount.value/100))

        if base_price < 0:
            return 0
        return base_price

    def get_final_price(self):
        return self.final_price

    def get_tags(self):
        return self.tags.all()

    def get_discounts(self):
        return self.discounts.all()


class ProductDiscount(models.Model):

    DISCOUNT_TYPES = [
        ('PERCENTAGE', 'porcentaje'),
        ('FIXED', 'plano'),
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=16, blank=False, unique=True)
    start_date = models.DateTimeField(default=timezone.now, null=False)
    end_date = models.DateTimeField(default=timezone.now, null=False)
    type = models.CharField(choices=DISCOUNT_TYPES, default='PERCENTAGE', max_length=32)
    value = models.FloatField(default=10)
    product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('start_date', )
        verbose_name = 'ProductDiscount'
        verbose_name_plural = 'ProductDiscounts'

    def __str__(self):
        return f"ProductDiscount(id={self.uuid}, code={self.code}, type={self.type}, value={self.value})"

    @property
    def active(self):
        return self.start_date <= timezone.now() <= self.end_date


class ProductTag(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    tag = models.CharField(max_length=64, null=False)
    active = models.BooleanField(default=False)
    product = models.ForeignKey(Product, related_name='tags', on_delete=models.CASCADE)

    class Meta:
        ordering = ('tag', )
        verbose_name = 'ProductTag'
        verbose_name_plural = 'ProductTags'

    def __str__(self):
        return f"ProductTag(id={self.uuid}, tag={self.tag})"
