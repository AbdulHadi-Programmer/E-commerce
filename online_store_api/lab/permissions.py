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

from rest_framework.permissions import BasePermission, SAFE_METHODS

# It restrict the user to not to publish the Article mean the book model one attribute 

class CanPublishBook(BasePermission):
    """
    Only staff/admin users can mark an article as published. (Article mean Book)
    Normal users can edit everything else but cannot set is_published=True.
    """

    def has_permission(self, request, view):
        # Require authentication for any modifying action
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Allow safe methods always
        if request.method in SAFE_METHODS:
            return True

        # Check if user is trying to publish (setting True)
        is_trying_to_publish = str(request.data.get("is_published")).lower() in ["true", "1"]

        # Block if not staff and trying to publish
        if is_trying_to_publish and not request.user.is_staff:
            return False

        # Otherwise, normal update allowed
        return True
