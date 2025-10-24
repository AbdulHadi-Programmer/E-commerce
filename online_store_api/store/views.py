from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from .models import Product , Category, Customer
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from .models import * 
from .serializers import * 
from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User 
from rest_framework import generics, serializers, status 
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated 
from rest_framework import mixins 
from django.contrib.auth import get_user_model 
from accounts.models import User 
from store.serializers import CustomerSerializer 
from accounts.permissions import * 

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

## API View  (for all 3 models):
# class ProductAPIView(APIView):  Normal API View
#     """
#     GET -> List all products 
#     POST -> Create a new product 
#     """

#     def get(self, request):
#         print(">>> HIT ProductAPIView (LIST)")
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAPIView(APIView):
    """
    GET -->  get all the customer
    POST --> create a new customer
    """
    def get(self, request):
        customer = Customer.objects.all()
        serializers = CustomerSerializer(customer, many=True)
        return Response(serializers.data)
    
    def post (self, request):
        serializers = CustomerSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


class CategoryAPIView(APIView):
    """
    GET -->  get all the customer
    POST --> create a new customer
    """
    def get(self, request):
        category = Category.objects.all()
        serializers = CategorySerializer(category, many=True)
        return Response(serializers.data)
    def post(self, request):
        serializers = CategorySerializer(data=request.data)
        if serializers.is_valid():   # checks for validation errors 
            serializers.save()  # saves to db
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

# ======================================================================================================================================================
## Detail View (Get, Update, Delete)
from accounts.permissions import IsOwnerOrReadOnly

class ProductDetailAPIView(APIView):
    """
    GET → get a single product
    PUT → update product
    DELETE → delete product
    """
    # def get_object(self, pk):
    #     try:
    #         return Product.objects.get(pk=pk)
    #     except Product.DoesNotExist:
    #         return None 
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request, pk):
        print(">>> HIT ProductDetailAPIView (DETAIL)")
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        # Pass the existing product and the incoming data
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class CustomerDetailAPIView(APIView):
    """
    GET → Get a Single Customer
    PUT → Update customer
    PATCH → Partially Update a customer 
    DELETE → Delete Customer
    """ 
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        if not customer:
            return Response({'error': "Customer Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializers = CustomerSerializer(customer)
        return Response(serializers.data)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response({"message": "Customer Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


## Category Detail View
class CategoryDetailAPIView(APIView):
    """
    GET → Retrieve category
    PUT → Update category
    PATCH → Partially update category
    DELETE → Delete category
    """

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)  # By using this we avoid writing same code again and again 
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# =====================================================================================================================
#            GenericAPIView + Mixins :
# =====================================================================================================================

# Product Mixins View:
class ProductListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    generics.GenericAPIView = queryset, serializer, get_serializer()
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 

    # HTTP GET → list()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # HTTP POST → create()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# DetailAPIView class inherit the mixins:  Retrive + Update + Delete :
class ProductDetailMixinView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs) 
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs )
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Category Mixins View :
class CategoryListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    # GET Method to get 
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # POST Method to post 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Category Detail View :        
class CategoryDetailMixinView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Category 
    serializer_class = CategorySerializer    
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs) 
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs )
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



# Customer Mixins View: 
class CustomerListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Customer
    serializer_class = CustomerSerializer 

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
# Customer Detail View :        
class CustomerDetailMixinView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Customer 
    serializer_class = CustomerSerializer    

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs) 
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs )
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer


class ProductAPIView(APIView):
    """
    GET -> Customers & Sellers can view
    POST -> Only Sellers can add products
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_seller:
            return Response({"error": "Only sellers can add products."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



############################################################################################################################################
#     CONCRETE GENERIC API View  (Optional: Skipping for now)
############################################################################################################################################

## 22 October 2025
### Permission Added New View : 
# Sellers can add or update products 
class SellerProductView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request): 
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(seller = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        product = Product.objects.get_object_or_404(pk=pk)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Customers can view only Products
class CustomerProductListView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

