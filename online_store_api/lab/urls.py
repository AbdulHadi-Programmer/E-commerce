# from .views import ProductViewSet, CategoryViewSet, CustomerViewSet , ProductAPIView, CustomerAPIView, CategoryAPIView, ProductDetailAPIView, CategoryDetailAPIView, CustomerDetailAPIView, ProductListCreateAPIView, CategoryListCreateAPIView, CustomerListCreateAPIView, ProductDetailMixinView, CategoryDetailMixinView, CustomerDetailMixinView, SellerProductView, CustomerProductListView
from django.urls import path, include 
# from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)
from .views import BookAPIView, BookDetailAPIView, AuthorAPIView, AuthorDetailAPIView

# url of this view start from  "lab/" 
urlpatterns = [
    path('books/', BookAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='update-delete'),
    path('author/', AuthorAPIView.as_view(), name='author-list-create'),
    path('author/<int:pk>/', AuthorDetailAPIView.as_view(), name='update-delete'),
]