from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone=models.CharField( max_length=50)
    street_address=models.CharField( max_length=200)


class Profile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='profile')
    profile_picture=models.ImageField(upload_to="profile_images")
    bio=models.TextField()
    dob=models.DateField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)