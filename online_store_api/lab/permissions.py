from rest_framework.permissions import BasePermission, SAFE_METHODS 


class IsAuthorOrReadOnly(BasePermission):
    """
    Allow authors to edit thier own books.
    Only the author can edit or delete thier own article.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True 
        # Otherwise, require authentication 
        return bool(request.user and request.user.is_authenticated)
        
    def has_object_permission(self, request, view, obj):
        # Safe Methods (GET, HEAD, OPIONS) always allowed 
        if request.method in SAFE_METHODS :
            return True 
        # Only author can modify 
        return obj.author == request.user

    
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True 
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True 
        return bool(request.user and obj.author.is_staff)


# Write your own version of CanPublishArticle (don't just copy mine)

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
