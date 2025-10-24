from django.contrib.auth import get_user_model 
from store.models import Customer 
from rest_framework import serializers
from .models import *

User = get_user_model()

# Create a Register Serializer :
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, min_length=4)
#     """
#     write_only=True: means password will never show up in responses.
#     create_user(): Django’s built-in function that automatically hashes passwords.
#     min_length=4: ensures user enters a password with at least 4 chars.
#     """
#     class Meta:
#         model = User 
#         fields = ['username', 'password']

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username Already exists")
#         return value 

#     def create(self, validated_data):
#         # create_user() automatically hashes password 
#         user = User.objects.create_user(
#             username = validated_data["username"],
#             password = validated_data["password"]
#         )
#         return user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=4)
    is_customer = serializers.BooleanField(default=True)
    is_seller = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_customer", "is_seller"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        if user.is_customer:
            Customer.objects.create(user=user, age=18)  # default age or handle later
        return user

# Profile Serializer : 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["username", "email", "is_seller", "is_customer"]

        
    

