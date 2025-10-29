from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response 
from rest_framework import status 
from .permissions import CanPublishBook, IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .pagination import BookPagination, AuthorPagination
from django.db.models import Q 

class BookAPIView(APIView):
    """
    GET:
      - Pagination
      - Search & Filter Books manually using query params:
        ?search=keyword
        ?genre=Fiction
        ?year=2024
        ?published=true
        ?order_by=latest|price_ascpass|price_desc
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all().order_by('-created_at')

        # --- Search ---
        search_query = request.GET.get('search')
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__name__icontains=search_query)
            )

        # --- Genre filter ---
        genre = request.GET.get('genre')
        if genre:
            books = books.filter(genre__iexact=genre)

        # --- Year filter ---
        year = request.GET.get('year')
        if year and year.isdigit():
            books = books.filter(published_year=int(year))

        # --- Published filter ---
        published = request.GET.get('published')
        if published:
            if published.lower() == 'true':
                books = books.filter(published=True)
            elif published.lower() == 'false':
                books = books.filter(published=False)

        # --- Ordering ---
        order_by = request.GET.get('order_by')
        if order_by == 'latest':
            books = books.order_by('-created_at')
        elif order_by == 'price_asc':
            books = books.order_by('price')
        elif order_by == 'price_desc':
            books = books.order_by('-price')

        # --- Pagination ---
        paginator = BookPagination()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

        
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, CanPublishBook]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        # Important: explicity check object permissions
        # This triggers your has_object_permission() 
        self.check_object_permissions(request, book)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        # Important: explicity check object permissions
        # This triggers your has_object_permission() 
        self.check_object_permissions(request, book)

        serializer = BookSerializer(book, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        # Perform any Necessary checks or permissions here
        # For Example, check if the requesting data is authorized to delete or the owner is authorized to delete this object
        # if request.user != book.author:
        #     return Response({"detail": "You do not have permission to delete this object."},
        #                     status=status.HTTP_403_FORBIDDEN)
        # Delete the object
        book.delete()

        # Return a success response
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        author = Author.objects.all()
        # More Search Order Filter logic could/will be added soon

        paginator = AuthorPagination()
        paginated_author = paginator.paginate_queryset(author, request)
        serializer = AuthorSerializer(paginated_author, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request) :
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AuthorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        self.check_object_permissions(request, author)
        serializer = AuthorSerializer(author)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        author = get_object_or_404(Author, pk=pk )
        serializer = AuthorSerializer(author, data=request.data)   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        author = get_object_or_404(Author, pk=pk)

        serializer = AuthorSerializer(author, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Currently it is simple delete, later we can add more access control to prevent everyone to avoid changing using DELETE method
    def delete(self, request, pk):  
        author = get_object_or_404(Book, pk=pk)
        author.delete()

        # Return a success response
        return Response(status=status.HTTP_204_NO_CONTENT)