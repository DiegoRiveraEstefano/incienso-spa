from django.contrib import admin
from .models import Cart, ProductCart

# Register your models here.

admin.site.register(Cart)
admin.site.register(ProductCart)