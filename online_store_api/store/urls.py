from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, CustomerViewSet , ProductAPIView, CustomerAPIView, CategoryAPIView, ProductDetailAPIView, CategoryDetailAPIView, CustomerDetailAPIView, ProductListCreateAPIView, CategoryListCreateAPIView, CustomerListCreateAPIView, ProductDetailMixinView, CategoryDetailMixinView, CustomerDetailMixinView
from django.urls import path, include 


# ModelViewSet URL:
router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("customers", CustomerViewSet)

urlpatterns = [
    # path("api/", include(router.urls)),
    # Single API View for all the models 

    # path("api/product_APIView/", ProductAPIView.as_view(), name="product-list"),
    # path("api/customer_APIView/", CustomerAPIView.as_view(), name="customer-list"),
    # path("api/category_APIView/", CategoryAPIView.as_view(), name="category-list"),

    # Detail View URLS:
    # path("api/product_APIView/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    # path("api/category_APIView/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    # path("api/customer_APIView/<int:pk>/", CustomerDetailAPIView.as_view(), name="customer-detail"),

    # Generic APIView + Mixins Urls (All CRUD) :
    # List and Create Method url : 
    path("product_mixins/", ProductListCreateAPIView.as_view(), name="all-product-mixin"),
    path("category_mixins/", CategoryListCreateAPIView.as_view(), name="all-category-mixin"),
    path("customer_mixins/", CustomerListCreateAPIView.as_view(), name="all-customer-mixin"),

    # Detail Mixins URLs:
    path("product_mixins/<int:pk>", ProductDetailMixinView.as_view(), name="all-product-mixin-detail"),
    path("category_mixins/<int:pk>", CategoryDetailMixinView.as_view(), name="all-category-mixin-detail"),
    path("customer_mixins/<int:pk>", CustomerDetailMixinView.as_view(), name="all-customer-mixin-detail"),
    
    
]
