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

class ProductTag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(ProductTag)

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
        