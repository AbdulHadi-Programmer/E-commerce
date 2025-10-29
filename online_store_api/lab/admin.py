from django.contrib import admin
from .models import Author, Book 
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user__username', 'bio']
    list_editable = ('name', )    

    list_display_links = ('id', )

admin.site.register(Author, AuthorAdmin)


class BookAdmin (admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'author', 'published', 'created_at']
    list_editable = ('published', 'price', 'author')
    list_filter = ('author', 'created_at', 'published')

admin.site.register(Book, BookAdmin)