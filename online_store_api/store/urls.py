from .views import ProductViewSet, CategoryViewSet, CustomerViewSet , ProductAPIView, CustomerAPIView, CategoryAPIView, ProductDetailAPIView, CategoryDetailAPIView, CustomerDetailAPIView, ProductListCreateAPIView, CategoryListCreateAPIView, CustomerListCreateAPIView, ProductDetailMixinView, CategoryDetailMixinView, CustomerDetailMixinView, SellerProductView, CustomerProductListView
from django.urls import path, include 
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)



urlpatterns = [
    # Single API View for all the models 

    # Detail View URLS:
    path("product_APIView/", ProductAPIView.as_view(), name="product-list"),
    path("product_APIView/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    
    path("customer_APIView/", CustomerAPIView.as_view(), name="customer-list"),
    path("customer_APIView/<int:pk>/", CustomerDetailAPIView.as_view(), name="customer-detail"),
    
    path("category_APIView/", CategoryAPIView.as_view(), name="category-list"),
    path("category_APIView/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),


    # Generic APIView + Mixins Urls (All CRUD) :
    # List and Create Method url : 
    # path("product_mixins/", ProductListCreateAPIView.as_view(), name="all-product-mixin"),
    # path("category_mixins/", CategoryListCreateAPIView.as_view(), name="all-category-mixin"),
    # path("customer_mixins/", CustomerListCreateAPIView.as_view(), name="all-customer-mixin"),

    # Detail Mixins URLs:
    # path("product_mixins/<int:pk>", ProductDetailMixinView.as_view(), name="all-product-mixin-detail"),
    # path("category_mixins/<int:pk>", CategoryDetailMixinView.as_view(), name="all-category-mixin-detail"),
    # path("customer_mixins/<int:pk>", CustomerDetailMixinView.as_view(), name="all-customer-mixin-detail"),
    
    # JWT auth buildin urls:  (URLs in accounts)
    #  Login (JWT)
    # path('register/', RegisterAPIView.as_view(), name="register"),
    # path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    # # New profile authenticated view: 
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('change-password/', ChangePasswordAPIView.as_view(), name="change-password")
    path('seller/products/', SellerProductView.as_view()),
    path('seller/products/<int:pk>/', SellerProductView.as_view()),
    path('customer_products/', CustomerProductListView.as_view()), 

]
