# lab/models.py
from django.db import models
from django.conf import settings
from accounts.models import User

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
