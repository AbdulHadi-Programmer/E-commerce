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
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_products")

    def __str__(self):
        return self.name

# Customer :
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    age = models.PositiveIntegerField()
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username 
    




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


