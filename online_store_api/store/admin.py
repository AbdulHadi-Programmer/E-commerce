from django.contrib import admin
from .models import Product, Category , Customer

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discounted_price', 'category', 'seller']

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
