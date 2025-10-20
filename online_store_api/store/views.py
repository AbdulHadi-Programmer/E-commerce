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
from rest_framework import generics, mixins 
from django.contrib.auth import get_user_model 


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
class ProductAPIView(APIView):
    """
    GET -> List all products 
    POST -> Create a new product 
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print(">>> HIT ProductAPIView (LIST)")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


############################################################################################################################################
#     CONCRETE GENERIC API View  (Optional: Skipping for now)
############################################################################################################################################
from rest_framework.permissions import AllowAny

## Authentication using JWT :
class RegisterAPIView(generics.CreateAPIView):  # Import the create Api view from Generics
    User = get_user_model()
    queryset = User.objects.all()   
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens automatically after registration 
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data, 
            "refresh": str(refresh),
            "access": str(refresh.access_token),  
        }, status = status.HTTP_201_CREATED)
    

# Protecting the endpoints:

class ProfileView(APIView):
    # permission_classes= [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username, 
            "email": user.email 
        })

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
