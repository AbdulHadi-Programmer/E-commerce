# from rest_framework import serializers
# from .models import Product, Category , Customer

# """
# ### 🎯 Your Task (Practice)

# 1. Add a field age to your Customer model (IntegerField).

# 2. Update your CustomerSerializer:
#   - Write a field-level validation so `age >= 18`.
 
# 3. Add a field discount_price to Product model (DecimalField, nullable).

# 4. Update your ProductSerializer:
#   - Add object-level validation so `discount_price < price`."""
# # from .serializers import CategorySerializer

# class ProductSerializer(serializers.ModelSerializer):
#     products = CategorySerializer(read_only=True)

#     class Meta:
#         model  = Product
#         # fields = "__all__"
#         fileds = ["name", "price", "discounted_price", "products"]

#     def validate_price(self, value):
#         if value < 1:
#             raise serializers.ValidationError("Price must be at least 1")
#         return value

#     def validate(self, data):
#         price = data.get("price")
#         discounted_price = data.get("discounted_price")
#         if discounted_price and discounted_price >= price:
#             raise serializers.ValidationError(
#                 "Discounted price must be less than the price"
#             )                
#         return data

# class CategorySerializer (serializers.ModelSerializer): 
#     # products = serializers.PrimaryKeyRelatedField(many=True, read_only=True )   # show id of product that is linked to this model
#     products = ProductSerializer(many=True, read_only=True)    # show complete data of product info 
    
#     class Meta :
#         model = Category 
#         # fields = "__all__"
#         fields = ["name", "products"]

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = "__all__"
    
#     def create(self, validated_data):
#         validated_data["name"] = validated_data["name"].title()
#         return super().create(validated_data)

#     # Field-level validation (age must be >= 18)
#     def validate_age(self, value):
#         if value < 18:
#             raise serializers.ValidationError("Age must be at least 18")
#         return value


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

# --- CUSTOMER SERIALIZER ---
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        validated_data["name"] = validated_data["name"].title()
        return super().create(validated_data)

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Age must be at least 18")
        return value
