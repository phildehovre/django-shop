from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pictures')
    bio=models.TextField(default='')

    def __str__(self):
        return self.user.username

class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200, default='Default address')
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    postcode=models.CharField(max_length=100)
    country=models.CharField(max_length=200)
    additional=models.TextField()
    default=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.address}"
    
    def save(self, *args, **kwargs):
    # Check if there's already a default address for this user
        if self.default:
            # Unset default flag for other addresses of the same user
            Address.objects.filter(user=self.user, default=True).exclude(pk=self.pk).update(default=False)
        super().save(*args, **kwargs)

