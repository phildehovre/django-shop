from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

RATING = (
    (1, "Terrible"),
    (2, "Poor"),
    (3, "Average"),
    (4, "Good"),
    (5, "Excellent"),
)
ORDER_STATUS = (
    (0, "INERT"),
    (1, "PENDING"),
    (2, "PROCESSING"),
    (3, "SHIPPED"),
    (4, "COMPLETED"),
)

class ProductTag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(default='https://www.eag-led.com/wp-content/uploads/2017/04/Product-Image-Coming-Soon.png', upload_to='media/products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(ProductTag)
    stock = models.IntegerField(default=999)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUS, default=0) 

    def __str__(self):
        return f"{self.user.username} -({self.quantity}) {self.product.name}"
    
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"