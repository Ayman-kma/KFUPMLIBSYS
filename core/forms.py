from django import forms
from .models import Book

class BookSearchForm(forms):
    
    class Meta:
        model = Book
        fields = ('book_title', 'subject', 'authors', 'publication_year')