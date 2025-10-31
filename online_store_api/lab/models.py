# lab/models.py
from django.db import models
from django.conf import settings
from accounts.models import User
from django.contrib.auth import get_user_model 
import uuid
import os

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_profile")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    # 🆕 Added fields for search/filter practice:
    genre = models.CharField(max_length=100, default="General")   # default genre
    published_year = models.IntegerField(default=2024)            # default year
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, default="Drama")
    release_year = models.IntegerField(default=2024)
    rating = models.FloatField(default=5.0)
    duration = models.IntegerField(default=120)  # minutes
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Course(models.Model):
    name = models.CharField(max_length=150)
    instructor = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="General")
    duration_weeks = models.PositiveIntegerField(default=4)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    level = models.CharField(max_length=50, default="Beginner")  # Beginner / Intermediate / Advanced
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

User = get_user_model()


# Utility function to rename uploaded files uniquely
def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"  # Rename file to UUID
    return os.path.join('uploads/', filename)


# ---------- LEVEL 2: Multiple Upload Example ----------
class Album(models.Model):
    """A collection of photos uploaded by a user"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Album: {self.name}"


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo in {self.album.name}"
