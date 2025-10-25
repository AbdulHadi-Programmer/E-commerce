from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSeller(BasePermission):
    """Allow access only to users with is_seller=True."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)


class IsCustomer(BasePermission):
    """Allow access only to users with is_customer=True."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer)


class IsOwnerOrReadOnly(BasePermission):
    """
    Only owner (seller) of a product can edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.seller == request.user

# 🧩 Task 1:
# Create a custom permission IsAdminOrReadOnly that:
# Allows admins full access.
# Allows normal users only GET methods.
class IsAdminOrReadOnly(BasePermission):
    """
    Allow full access to admin users (is_superuser=True).
    Allow read-only (GET, HEAD, OPTIONS) to everyone else.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsSeller(BasePermission):
    """Allow access only to sellers"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller) 


"""
🔍 Step 5: Practice Tasks

🧩 Task 1:
Create a custom permission IsAdminOrReadOnly that:
Allows admins full access.
Allows normal users only GET methods.

🧩 Task 2:
Allow only customers to place orders (we’ll create an Order model later).

🧩 Task 3:
Modify the register API so that user can choose role — seller or customer.

🧩 Task 4:
Restrict product deletion — only the product’s seller can delete it.

🧩 Task 5:
Add pagination and filtering for customer product listing (tomorrow’s topic 👀).
"""
# latest 24 Oct 9 pm 
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MTkyNTMyMCwiaWF0IjoxNzYxMzIwNTIwLCJqdGkiOiI4ZjdlODJkOGI2ZDQ0YmFjOTMxNTAwNWUzNzM0ZWQ2ZSIsInVzZXJfaWQiOiIxIn0.D-rOWyiQsJ4nVV9Mwe6VdxXbIt4e0JgRokTDdj9-ArQ",

    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNDA2OTIwLCJpYXQiOjE3NjEzMjA1MjAsImp0aSI6IjJhNDlmNDZkODY3MzRmNGE4ZWFkOTUxYTRjYjU1MGNkIiwidXNlcl9pZCI6IjEifQ.pibTxL3nCN85E5kpHWrxVF9nJ4tcxlf09y2Zo9W47WE"
}