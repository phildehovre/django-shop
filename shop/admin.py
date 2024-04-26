from django.contrib import admin

# Register your models here.

from .models import Product, ProductTag, OrderItem, Order

admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(Order)
admin.site.register(OrderItem)

