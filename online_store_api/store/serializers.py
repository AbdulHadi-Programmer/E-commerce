from rest_framework import serializers
from .models import Product, Category , Customer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

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

"""
### 🎯 Your Task (Practice)

1. Add a field age to your Customer model (IntegerField).

2. Update your CustomerSerializer:
  - Write a field-level validation so `age >= 18`.
 
3. Add a field discount_price to Product model (DecimalField, nullable).

4. Update your ProductSerializer:
  - Add object-level validation so `discount_price < price`."""
class CategorySerializer (serializers.ModelSerializer): 
    class Meta :
        model = Category 
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
    
    def create(self, validated_data):
        validated_data["name"] = validated_data["name"].title()
        return super().create(validated_data)

    # Field-level validation (age must be >= 18)
    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Age must be at least 18")
        return value










