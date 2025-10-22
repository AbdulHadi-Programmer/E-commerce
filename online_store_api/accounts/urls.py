from django.urls import path 
from .views import RegisterAPIView, ProfileView, LogoutView, ChangePasswordAPIView
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)

urlpattern = [
    # JWT auth buildin urls:
    #  Login (JWT)
    path('register/', RegisterAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    # New profile authenticated view: 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name="change-password")
]