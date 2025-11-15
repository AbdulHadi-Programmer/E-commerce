from django.db import models
from accounts.models import User
from django.conf import settings

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
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# Customer :
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    age = models.PositiveIntegerField()
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username 
    
# Order 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.customer.username}'
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity 
        super().save(*args, **kwargs) 

