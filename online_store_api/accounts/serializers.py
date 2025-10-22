from django.contrib.auth import get_user_model 
from store.models import Customer 
from rest_framework import serializers
from .models import *

User = get_user_model()

# Create a Register Serializer :
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=4)
    """
    write_only=True: means password will never show up in responses.
    create_user(): Django’s built-in function that automatically hashes passwords.
    min_length=4: ensures user enters a password with at least 4 chars.
    """
    class Meta:
        model = User 
        fields = ['username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username Already exists")
        return value 

    def create(self, validated_data):
        # create_user() automatically hashes password 
        user = User.objects.create_user(
            username = validated_data["username"],
            password = validated_data["password"]
        )
        return user

