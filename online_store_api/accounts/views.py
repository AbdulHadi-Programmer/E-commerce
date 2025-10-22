from django.shortcuts import render
from store.serializers import RegisterSerializer
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated 
from rest_framework import mixins 
from django.contrib.auth import get_user_model 
from rest_framework.response import Response 
from rest_framework.views import APIView  
from .permissions import IsSeller, IsCustomer 
from accounts.models import User
from store.serializers import CustomerSerializer 

# Create your views here.
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
            "email": user.email,
            'is_seller': user.is_seller,
            "is_customer": user.is_customer
        })

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)

# GPT what can i do i have more luxury premium dream in my mind like this above workshop session in school idea, freelancing idea, job idea in big company idea, doing a physical or online business idea what can i do 
