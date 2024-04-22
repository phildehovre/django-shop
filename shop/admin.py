from django.contrib import admin

# Register your models here.

from .models import Product, Review, ProductTag, Basket, Order

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ProductTag)
admin.site.register(Basket)
admin.site.register(Order)