# 27 Oct 2025 
## Step 1 -- Reset the Context 
`author` →  the user who owns the book 
`is_published` →  whether the book is public 
`is_published` →  should only be editable by admins

## Step 2 —— The Real Question I Asked 
"How can I restrict a user from editing the specific  field — like `is_published` —— unless they are an admin?" 
This is not about object ownership anymore.
It's **field-level permission** (which is advance, and you're doing it right).

## Step 3 —— The Core Idea Behind Restricting a Field 
You can't stop users from sending `"is_published": true`
—— but you can block the request before saving based on what they sent.

So inside a permission, we check:
> "Did the user try to set `is_published` to `True`?"
If yes → allow only if they are admin.

## Step 4 —— What check_object_permissions() Actually Is 
This is not a random function; it comes from DRF's APIView base class.
- DRF automatically calls `has_permission()` before your view runs.
- But it does NOT automatically call `has_object_permission()` in `APIView`.
That only happens in ViewSets and mixins.

So if you want `has_object_permission()` to run inside you own `APIView`.
You must call it manually like this :
```py
self.check_object_permissions(request, obj)
```

This line tells DRF:
> Run all has_object_permission() check for this object.
If the permission fails, DRF automatically returns a 403 Forbidden response.

# Step —— Clean, Correct CanPublishBook Permission 
```py
# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class CanPublishBook(BasePermission):
    """
    Only admins can set a book as published.
    Normal authors can edit everything else.
    """

    def has_permission(self, request, view):
        # Everyone must be authenticated to modify anything
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests
        if request.method in SAFE_METHODS:
            return True

        # Get what the user is trying to update
        is_trying_to_publish = str(request.data.get("is_published")).lower() in ["true", "1"]

        # If trying to publish but not admin → deny
        if is_trying_to_publish and not request.user.is_staff:
            return False

        # Otherwise allow normal edits (title, description)
        return True

```