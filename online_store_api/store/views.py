from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from .models import Product , Category, Customer
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer
# Create your views here.

# ModelViewSet is the easiest way to write CRUD in 3 lines only 
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer 

