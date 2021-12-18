import django_filters 
from .models import Book

class BookFilter(django_filters.FilterSet):

    book_title = django_filters.CharFilter(lookup_expr='icontains')
    # subject = django_filters.Filter(lookup_expr='icontains')
    # authors = django_filters.Filter(lookup_expr='icontains')
    publication_year = django_filters.CharFilter()
    class Meta:
        model =  Book
        fields = ('book_title', 'subject', 'authors', 'publication_year')