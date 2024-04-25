from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='media/profile_images')

    def __str__(self):
        return self.user.username
