from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Address(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    number=models.CharField(max_length=5)
    street=models.CharField(max_length=50)
    postcode=models.CharField(max_length=10)
    city=models.CharField(max_length=50)
    country=models.CharField(max_length=50)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    bio=models.TextField()
    address=models.OneToOneField(Address, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/profile')


    def __str__(self):
        return self.user.username