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
        fields = ['title', 'description', 'price','author', 'author_name', 'genre', 'published', 'published_year']

    def validate_published(self, value):
        request = self.context['request']
        if value and not request.user.is_staff: 
            raise serializers.ValidationError("Only admin can publish books")
        return value 
    
