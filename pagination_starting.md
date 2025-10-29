## 27 Oct 11:36 pm (Mid-Night)
## Step 1 —— What Pagination Actually Is 
**Problem :**
When you have 1000+ rows in your database (like Book.objects.all()), returning all of them in one API call is inefficient. 

**Solution :**
Pagination breaks large querysets into smaller chunks — pages —— that clients can requesst piece by piece.

Example:
GET /book/?page=2  → returns page 2 of results.


## Step 2 —— Two Ways DRF Does Pagination
1. Global Pagination (settings.py)
- Automatically applies to all List endpoints if you use generics or Viewsets.
- You don't want this now, since you're using APIView.
2. Manual Pagination (APIView)
- You instantiate a paginator manually inside your view.
- You control exactly when and how pagination is applied.

## Step 3 —— Import and Setup 
Use DRF's built-in paginator:
```py
from rest_framework.pagination import PageNumberPagination
# Now create your own paginator class —— this lets you control page sizes, limits etc.

# lab/permissions.py
class BookPagination(PageNumberPagination):
    page_size = 5                   # Default numbers of items per page
    page_size_query_param = 'size'  # Client can override ?size=10
    max_page_size = 50              # Prevent abuse (too large)

```

## Step 4 —— Implement It in APIView 
Here's how you use it inside a BookListView:


```py
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import EmptyPage
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer
from .pagination import BookPagination

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all().order_by('-created_at')
        paginator = BookPagination()
        
        # Apply pagination to the queryset
        paginated_books = paginator.paginate_queryset(books, request)
        
        serializer = BookSerializer(paginated_books, many=True)
        
        # Return a paginated response
        return paginator.get_paginated_response(serializer.data)
```


How to Use it in the Browser 
Examples:
1. GET /lab/book/                    <!-- return first 5 books -->
2. GET /lab/book/?page=2             <!-- return next 5 books -->
3. GET /lab/book/?size=10            <!-- return 10 per page -->
4. GET /lab/book/?page=3&size=10     <!-- return page 3, 10 per page -->

### If you want simpler pagination for the other API's
Instead of writing all this in every view, you can: 
1. Create a global setting in settings.py: 
