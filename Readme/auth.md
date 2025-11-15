# Custom User Model (DRF + JWT) — Step-by-Step Guide

## Step 1 — Define Custom User Model

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
is_seller = models.BooleanField(default=False)
is_customer = models.BooleanField(default=True)

def __str__(self):
return self.username
```

## Step 2 — Update Settings

In `settings.py`:

```python
AUTH_USER_MODEL = "store.User"
```

##  Step 3 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

If migration issues occur:
```bash
rm db.sqlite
find. -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

##  Step 4 — Update Register Serializer

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=4)

class Meta:
    model = User
    fields = ['username', 'password', 'is_customer', 'is_seller']

def create(self, validated_data):
    user = User.objects.create_user(
    username=validated_data['username'],
    password=validated_data['password'],
    is_customer=validated_data.get('is_customer',   True),
    is_seller=validated_data.get('is_seller', False)
    )
    return user
```

## Step 5 — Register API View

```python
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

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

## n Step 6 — Test in Postman

**POST → `/api/register/`**
```json
{
"username": "shopowner",
"password": "1234",
"is_seller": true,
"is_customer": false
}
```

**POST → `/api/register/`**
```json
{
"username": "customer1",
"password": "1234",
"is_customer": true
}
```


## Step 7 — Verify in Django Shell

```bash
python manage.py shell
```

```python
from store.models import User
User.objects.all()
```

#  Next Step — Level 2: Role-Based Permissions
- Sellers → can create/update/delete products
- Customers → can only view products
- Admin → can do everything


