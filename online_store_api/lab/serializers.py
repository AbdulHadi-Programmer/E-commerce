from rest_framework import serializers
from .models import Book, Author , Movie, Course, Profile, Album, Photo


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
    
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie 
        fields = ['title', 'director','genre','release_year','rating','duration' ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course 
        fields = ['name', 'instructor', 'category', 'duration_weeks', 'price', 'level']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Profile 
        fields = ['id', 'user', 'bio', 'image']
        read_only_fields = ['user']



class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'uploaded_at']


class AlbumSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'photos']
        # read_only_fields = ['created_by']

