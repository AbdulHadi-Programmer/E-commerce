from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response 
from rest_framework import status 

class BookAPIView(APIView):

    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(Book, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = BookSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(request.errors, status=status.HTTP_400_BAD_REQUEST)


