from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='media/profile_pictures/default.jpg', upload_to='media/profile_pictures')
    bio=models.TextField(default='')

    def __str__(self):
        return self.user.username

class Address(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200, default='Default address')
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    postcode=models.CharField(max_length=100)
    country=models.CharField(max_length=200)
    additional=models.TextField()