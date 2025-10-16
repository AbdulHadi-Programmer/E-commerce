## 15 October 2025 :

## Day 3 of Challenge :
### **Goal:**
- Understand GenericAPIView as a flexible foundation
- Learn Mixins to avoid repeated CRUD code 
- Build clean, maintable APIViews for all models
- Compare with APIView and see why DRF generics are better for standard CRUD

## 1️⃣ GenericAPIView Overview
`GenericAPIView` is a base class in DRF that provides:
- Core functionality for queryset & serializer handling
- Methods like `get_queryset()` and `get_serializer()`
- Lookup logic for a single object (`lookup_field`, usually `pk`)
- Hooks like `perform_create()`, `perform_update()`, `perform_destroy()`

But it does not implement HTTP methods (`get`, `post`, `put`, etc.) itself. That’s where Mixins come in.
Think of it like a **toolbox:** GenericAPIView gives the structure; Mixins give the tools (actions).

## 2️⃣ DRF Mixins Overview
DRF Mixins provide reusable action logic:

| Mixin                | Provides Method                    |
| -------------------- | ---------------------------------- |
| `CreateModelMixin`   | `create()` → POST                  |
| `ListModelMixin`     | `list()` → GET (list of objects)   |
| `RetrieveModelMixin` | `retrieve()` → GET (single object) |
| `UpdateModelMixin`   | `update()` → PUT / PATCH           |
| `DestroyModelMixin`  | `destroy()` → DELETE               |

You can mix them into GenericAPIView to get only the functionality you need.

## 