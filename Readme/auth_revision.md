# 🧠 JWT Authentication + Permissions — Complete Revision (DRF Level 1–2)

## 🚀 Overview
In modern backend systems (like our online store API), **Authentication** and **Authorization** form the backbone of secure APIs.

- **Authentication** → “Who are you?”  
- **Authorization** → “What are you allowed to do?”

We use **JWT (JSON Web Tokens)** for stateless authentication and **custom permissions** to control access.

---

## 🔑 JWT Authentication — Step-by-Step Summary

### 1. Custom User Model
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username
```

### 2. Register Serializer & API View
Handles new user registration and issues JWT tokens.

```python
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
```

### 3. Login API (Using JWT Views)
In `urls.py`:
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### 4. Profile API (Protected)
```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Welcome, {request.user.username}!"})
```

You must send your **Access Token** in headers:
```
Authorization: Bearer <your_access_token>
```

### 5. Blacklisting Refresh Token (Logout)
```python
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
```

---

## 🧩 Permissions System (Level 2)

### Built-in Permissions
- `AllowAny` → Anyone can access
- `IsAuthenticated` → Only logged-in users
- `IsAdminUser` → Only admin/superuser
- `IsAuthenticatedOrReadOnly` → Read for all, write for logged-in

### Custom Permissions Example
Only allow sellers to create new products.

```python
from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)
```

Use it in a view:
```python
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    ...
```

---

## 🧠 Practice Ideas
1. Create a **Change Password API** with old & new password validation.
2. Restrict **Product creation** to `is_seller=True` users.
3. Allow **Customers** to view products but not create them.
4. Implement a **profile update API** (PATCH request).
5. Try **IsOwnerOrReadOnly** permission for user-specific data.

---

## 🔗 Example Routes Overview

| Endpoint | Method | Description | Auth Required |
|-----------|---------|-------------|----------------|
| `/api/register/` | POST | Register new user | ❌ |
| `/api/login/` | POST | Get JWT access & refresh tokens | ❌ |
| `/api/token/refresh/` | POST | Refresh Access Token | ❌ |
| `/api/profile/` | GET | Get logged-in user info | ✅ |
| `/api/logout/` | POST | Blacklist refresh token | ✅ |
| `/api/products/` | GET | List products | ✅ |
| `/api/products/create/` | POST | Create product (Seller only) | ✅ |

---

## 🎯 Key Takeaways
- **JWT** is stateless and secure — no sessions on the server.
- **Access Token** expires fast; **Refresh Token** lives longer.
- Use **blacklist** to invalidate tokens on logout.
- Control user access via **permissions**.
- Always send `Authorization: Bearer <token>` in headers.

---