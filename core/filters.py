import django_filters 
from .models import Book

class BookFilter(django_filters.FilterSet):
    
    subject = django_filters.CharFilter()
    authors = django_filters.CharFilter()
    publication_year = django_filters.CharFilter()
    class Meta:
        model =  Book
        fields = ('book_title', 'subject', 'authors', 'publication_year')