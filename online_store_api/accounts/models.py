from django.db import models

# Create your models here.
## Authentication : 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model that extends Django's built-in AbstractUser.
    Useful for adding roles and future fields (like phone, address, etc.)
    """
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username