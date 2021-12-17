from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from django.http.response import HttpResponse
from .models import *
from .forms import borrowBookForm
from django.urls import reverse
from django.utils.http import urlencode



def index(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'core/index.html', context)


def register_new_member(request):
    context = {}
    return render(request, 'core/register-new-member.html', context)

def borrow(request):
 # if this is a POST request we need to process the form data
    valid_book_items = get_valid_book_items()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = borrowBookForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            redirect_url = reverse('core:borrowed-successful', args=(form.cleaned_data["book_item"].bar_code,))
            return redirect(f'{redirect_url}')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = borrowBookForm()
    home_url_list = request.build_absolute_uri().split("/")[:-2]
    home_url = "/".join(home_url_list)
    return render(
        request,
        'member/borrow.html',
        {'form': form,
        "valid_book_items": valid_book_items,
        "home_url": home_url})


def borrowed_successful(request, book_item):
    book_item_instance = get_object_or_404(Book_Item, pk=book_item)
    today = datetime.date.today()
    member = Member.objects.filter(user=request.user).first()
    loan = Book_Loan(
        borrower= member,
        book_item= book_item_instance,
        borrowed_from = today,
        borrowed_to =today + datetime.timedelta(days= 90),
        )
    loan.save()
    return render(request, 'member/borrowed-successful.html', {'book_item': book_item_instance})


def get_valid_book_items():
        valid_book_items= []
        book_codes= set()
        book_items = Book_Item.objects.all().prefetch_related("book")
        for book_item in book_items:
            # key-Display value pairs
            # Remove duplicate books with many book items and only display the first one.
            if book_item.loan_status and book_item.book.ISBN_code not in book_codes:
                book_codes.add(book_item.book.ISBN_code)
                valid_book_items.append(book_item)
        return valid_book_items