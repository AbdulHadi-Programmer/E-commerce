from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, CustomerViewSet 
from django.urls import path, include 


router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("customers", CustomerViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
