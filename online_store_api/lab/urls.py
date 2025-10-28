# from .views import ProductViewSet, CategoryViewSet, CustomerViewSet , ProductAPIView, CustomerAPIView, CategoryAPIView, ProductDetailAPIView, CategoryDetailAPIView, CustomerDetailAPIView, ProductListCreateAPIView, CategoryListCreateAPIView, CustomerListCreateAPIView, ProductDetailMixinView, CategoryDetailMixinView, CustomerDetailMixinView, SellerProductView, CustomerProductListView
from django.urls import path, include 
# from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)
from .views import BookAPIView, BookDetailAPIView, AuthorAPIView

# url of this view start from  "lab/" 
urlpatterns = [
    path('book/', BookAPIView.as_view(), name='book-list-create'),
    path('author/', AuthorAPIView.as_view(), name='author-list-create')
]