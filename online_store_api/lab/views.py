from .models import Book, Author, Movie, Course, Profile, Album, Photo 
from .serializers import BookSerializer, AuthorSerializer, MovieSerializer, CourseSerializer, ProfileSerializer, AlbumSerializer, PhotoSerializer
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
        # author = Author.objects.all()

        # --- Search ---
        search_query = request.GET.get('search')
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(author__bio__icontains=search_query )
            )

        # --- Genre filter ---
        # genre = request.GET.get('genre') # single data
        genres = request.GET.getlist('genre')
        if genres:
            books = books.filter(genre__in=genres)
            # books = books.filter(genre__iexact=genre) # Search single genre

        # -- Task 3 -Price Range Filtering
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price: 
            books = books.filter(
                Q (price__gte=min_price) | 
                Q (price__lte=max_price)
            )

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
    
## Movie and Course APIView : 
class MovieAPIView(APIView): 
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CourseAPIView(APIView):
    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
## Profile APIView 
class ProfileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user= request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
# Album PhotoUploadView
class AlbumAPIView(APIView):
    def get(self, request):
        album = Album.objects.all()
        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This below view can handle multiple image upload in single api request 
class AlbumPhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        album_id = request.data.get('album_id')
        if not album_id:
            return Response({'error': 'album_id is required'}, status=400)

        album = get_object_or_404(Album, id=album_id, created_by=request.user)
        files = request.FILES.getlist('images')

        if not files:
            return Response({'error': "No files provided"}, status=400)

        uploaded = []
        for f in files:
            photo = Photo.objects.create(album=album, image=f)
            uploaded.append(photo)

        serializer = PhotoSerializer(uploaded, many=True)
        return Response(serializer.data, status=201)

