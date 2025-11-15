## Permission : 
* Permissions answer: **“Is this request allowed?”**
* DRF runs permission checks before view code. `If they fail → 403`.

* Two hook methods on permission classes:
    - `has_permission(self, request, view)` — general checks before we know which object(s) are involved. Use for auth, role checks, method-level checks, action-level checks.
    - `has_object_permission(self, request, view, obj)` — object-level checks when you already identified the object (detail views, object-level actions). Use for owner-checks, per-object visibility.

* DRF calls has_permission() first; if the view then calls get_object() (detail view), DRF will call has_object_permission() for that object if the permission class implements it.

* Order matters: the first permission class that returns False will cause denial.

* Built-ins: AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions, DjangoObjectPermissions.

* Permissions are not authentication — they rely on request.user set by authentication.

## 2) When to use has_permission vs has_object_permission — concise rules

* Use `has_permission` when:
    * You only need to know who the requester is (roles, logged in, group membership).
    * You want to allow/deny entire actions like POST /create, or non-detail endpoints.
    * Example: “Only authenticated users may create resources”, “Only sellers can POST to /products/”.

* Use `has_object_permission` when:
    - Access depends on the specific object (ownership, per-object visibility, resource state).
    - Example: “Only the owner of the profile can edit it”, “Only the seller of a product can update it”, “A user can view an order only if they are the buyer or staff.”

* You typically implement both when you want a coarse-grain gate `(has_permission)` then finer-grain checks `(has_object_permission)`. E.g. `has_permission` requires logged-in + role, `has_object_permission` checks ownership.

## 3) Minimal examples — quick reference
Generic Permission skeleton

```py
from rest_framework.permissions import BasePermission

class IsSomething(BasePermission):
    def has_permission(self, request, view):
        # allow only authenticated users for non-read methods
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # object-level check
        return obj.owner == request.user
```

