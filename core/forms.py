from .models import Book
from django import forms
from .models import Book_Item


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, book_item):
        return f"Book Title: {book_item.book.book_title}, barcode: {book_item.bar_code}"


class borrowBookForm(forms.Form):

    def get_valid_barcodes():
        bar_codes = []
        book_codes = set()
        book_items = Book_Item.objects.all().prefetch_related("book")
        for book_item in book_items:
            # key-Display value pairs
            # Remove duplicate books with many book items and only display the first one.
            if book_item.loan_status and book_item.book.ISBN_code not in book_codes:
                book_codes.add(book_item.book.ISBN_code)
                bar_codes.append(book_item.bar_code)
        return bar_codes

    book_item = MyModelChoiceField(
        required=True,
        widget=forms.Select,
        queryset=Book_Item.objects.filter(
            bar_code__in=get_valid_barcodes()).prefetch_related("book"),
        empty_label="--------",
    )


class BookSearchForm(forms):

    class Meta:
        model = Book
        fields = ('book_title', 'subject', 'authors', 'publication_year')
