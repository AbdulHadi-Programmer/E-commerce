from rest_framework import serializers
from .models import Product, Category, Customer
# from . import ProductSerializer



# --- PRODUCT SERIALIZER ---
class ProductSerializer(serializers.ModelSerializer):
    # Show category name instead of category ID
    category_name = serializers.CharField(source="category.name", read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(source="category", queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ["name", "price", "discounted_price", "category_name", "category_id"]

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError("Price must be at least 1")
        return value

    def validate(self, data):
        price = data.get("price")
        discounted_price = data.get("discounted_price")
        if discounted_price and discounted_price >= price:
            raise serializers.ValidationError(
                "Discounted price must be less than the price"
            )
        return data

# --- CATEGORY SERIALIZER ---
class CategorySerializer(serializers.ModelSerializer):
    # Show all products linked to this category
    # products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["name", "products"]

# -------------- Customer Serializer ---------------
class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "username", "email", "age", "joined_date"]

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Age must be at least 18")
        return value
    
# # from django.contrib.auth.models import User 
# # from rest_framework import serializers
# from django.contrib.auth import get_user_model 
# User = get_user_model()
# from .models import Customer 

# # Create a Register Serializer :
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


