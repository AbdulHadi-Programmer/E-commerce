## 21 October
This level builds directly on what you already mastered __ now we'll use your custom user model to differentiate access between sellers and customers.
You'll learn how to make endpoints that:
- Sellers can create or edit product
- Customers can only view them 
- Admin can do everything

### Level 2 -- Roadmap :
| Step | Topic                          | Goal                                         |
| ---- | ------------------------------ | -------------------------------------------- |
| 1️⃣  | Roles & Permissions Overview   | Understand how Django permissions work       |
| 2️⃣  | Create Role-Based Permissions  | Build custom permissions for seller/customer |
| 3️⃣  | Apply Permissions to Views     | Secure endpoints properly                    |
| 4️⃣  | Test with JWT Tokens           | Validate permissions in Postman              |
| 5️⃣  | Practice & Interview Questions | Reinforce your learning                      |
|     |                                |                                              |  

## Step 1 -- Understanding Roles and Permissions
Before writing code, let's simplify the concepts:
 
| Concept    | Meaning             | Example     |
| ---------- | ------------------- | ----------- |
| Authentication | Confirms who you are | Logging in with JWT |
| Authorization (Permission) | Decides what you can do | Seller can add product, customer can't |
| Roles | User Categories | Seller, Customer, Admin |
|       |                 |                     |

## Step 2 -- Create Custom Permissions :
Let's create a file `permissions.py` in your main app (e.g: store/permissions.py):
```python
from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    """Allow access only to users with is_seller=True."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)


class IsCustomer(BasePermission):
    """Allow access only to users with is_customer=True."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer)
```

### Step 3 -- Apply Permission in Views:
Example for your ProductAPIView:
```python
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSeller, IsCustomer

class ProductAPIView(APIView):
    """
    GET -> Customers & Sellers can view
    POST -> Only Sellers can add products
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_seller:   # this line protect that seller only view the post or use this
            return Response({"error": "Only sellers can add products."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

## Bonus Tip : 
If you ever want to make permissions reusable instead of writing `if not request.user.is_seller:` everytime ——
you can define custom permissions in a file like `permissions.py`:

```py
from rest_framework.permissions import BasePermission
class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller )

# Then in your view:
permission_classes = [IsAuthenticated, IsSeller]
```

