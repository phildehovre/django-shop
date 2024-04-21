from django.contrib import admin

# Register your models here.

from .models import Product, Review, ProductTag

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ProductTag)