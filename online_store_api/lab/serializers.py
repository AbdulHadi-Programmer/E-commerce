from rest_framework import serializers
from .models import Book, Author 


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author 
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    class Meta:
        model = Book 
        fields = ['title', 'description' ,'price' ,'author', 'author_name', 'published']

