from django.db import models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name

# Customer :
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    joined_date = models.DateField(auto_now_add=True)




# class User(AbstractUser):
#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     def __str__(self):
#         return self.email 
    
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
#     address = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return self.user.email 



# {
#     "user": {
#         "username": "ahmad"
#     },
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MTQwNDkwOCwiaWF0IjoxNzYwODAwMTA4LCJqdGkiOiI5MjA4MjliNmY5OGM0ZTlhYWQ0N2U0MzI3NDg0NDZmZCIsInVzZXJfaWQiOiIxIn0.UOolGexeztODdIFa61IFQk41WJnrv71bPy0WpXQ9m3Q",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwODAzNzA4LCJpYXQiOjE3NjA4MDAxMDgsImp0aSI6IjViMWYxYTlmYTBlYjQ5YzZhMGZjYWIzNGY1ZTY3YTE2IiwidXNlcl9pZCI6IjEifQ.ItQcJkduHLSNjsSvKTTbblhObqRRYBHovfvtMP_2L1w"
# }