from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from django.http.response import HttpResponse
from .models import *
# from .forms import borrowBookForm
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.models import User

import pytz

from .filters import BookFilter
from django.views.generic import ListView


def index(request):
    context = {
        'books': Book.objects.all(),
    }
    return render(request, 'core/index.html', context)

def report_get_new_members(request):
    utc=pytz.UTC
    query1= Member.objects.all()
    today_one_year_ago = datetime.datetime.today() - datetime.timedelta(days = 365)
    valid_members = [x for x in query1 if x.date_joined> utc.localize(today_one_year_ago) and x.checked_out_books_previously]
    context = {
        'books': Book.objects.all(),
        "members": valid_members,
    }
    return render(request, 'reports/new-members.html', context)

def report_get_all_members(request):
    all_members = Member.objects.all().prefetch_related('user')
    dictionary = []
    for member in all_members:
        loans = Book_Loan.objects.filter(borrower=member)
        current_loans = [x for x in loans if not x.actual_return_date]
        penalty = 0
        for loan in current_loans:
            if(loan.borrowed_to<datetime.date.today()):
                days = datetime.date.today()-loan.borrowed_to
                days = days.days
                penalty += days*5
        dictionary.append({
            'member': member,
            'loans': current_loans,
            'penalty': penalty
        })  
    context = {
        'dictionary': dictionary,

    }
    return render(request, 'reports/all-members.html', context)

def report_return_before_due(request):
    all_members = Member.objects.all().prefetch_related('user')
    dictionaries = []
    for member in all_members: 
        boolean=False
        Loans = Book_Loan.objects.filter(borrower=member)
        for x in Loans:
           if(x.actual_return_date):
            if(x.borrowed_to>x.actual_return_date):
                boolean = True
        if(boolean):
            dictionaries.append({
                'member': member,
            })    
    context = {
        'dictionaries': dictionaries,
    }
    return render(request, 'reports/before-due.html', context)


def register_new_member(request):
    context = {}
    return render(request, 'core/register-new-member.html', context)


def borrow(request):
    current_member = Member.objects.filter(user=request.user).first()
    user_loans = Book_Loan.objects.filter(borrower= current_member)
    current_loans = [x for x in user_loans if not x.actual_return_date]
    home_url_list = request.build_absolute_uri().split("/")[:-2]
    home_url = "/".join(home_url_list)
    if len(current_loans) >= 5:
        return render(request, 'member/return.html',{
            "limit": True,
            "loans": current_loans,
            "home_url": home_url
        })
    valid_book_items = get_valid_book_items()
    return render(
        request,
        'member/borrow.html',
        {"valid_book_items": valid_book_items,
         "home_url": home_url})


def borrowed_successful(request, book_item):
    book_item_instance = get_object_or_404(Book_Item, pk=book_item)
    today = datetime.date.today()
    member = Member.objects.filter(user=request.user).first()
    loan = Book_Loan(
        borrower=member,
        book_item=book_item_instance,
        borrowed_from=today,
        borrowed_to=today + datetime.timedelta(days=30),
    )
    loan.save()
    return render(request, 'member/borrowed-successful.html', {'book_item': book_item_instance, "loan": loan})


def get_valid_book_items():
    valid_book_items = []
    book_codes = set()
    book_items = Book_Item.objects.all().prefetch_related("book")
    for book_item in book_items:
        # key-Display value pairs
        # Remove duplicate books with many book items and only display the first one.
        if book_item.loan_status and book_item.book.ISBN_code not in book_codes:
            book_codes.add(book_item.book.ISBN_code)
            valid_book_items.append(book_item)
    return valid_book_items


def reserve(request):
    home_url_list = request.build_absolute_uri().split("/")[:-2]
    home_url = "/".join(home_url_list)
    books = get_valid_reserves()
    return render(
        request,
        'member/reserve.html',
        {
            "books": books,
            "home_url": home_url
        })


def reserve_request(request, book):
    book_instance = get_object_or_404(Book, pk=book)
    today = datetime.date.today()
    member = Member.objects.filter(user=request.user).first()
    reserve = Book_Reserve(
        borrower=member,
        book=book_instance,
        reserve_date=today,
        reserve_status=False
    )
    reserve.save()
    return render(request, 'member/reserve-request.html', {'book': book_instance})


def get_valid_reserves():
    valid_books = []
    books = Book.objects.all()
    for book in books:
        book_items = Book_Item.objects.filter(book=book)
        book_is_available = False
        for item in book_items:
            if (item.loan_status):
                book_is_available = True
        if not book_is_available:
            valid_books.append(book)

    return valid_books

def get_valid_returns(request):
    member = Member.objects.filter(user=request.user).first()
    loans = Book_Loan.objects.filter(borrower=member).prefetch_related("book_item")
    return loans

def return_book(request):
    home_url_list = request.build_absolute_uri().split("/")[:-2]
    home_url = "/".join(home_url_list)
    loans = get_valid_returns(request)
    return render(
        request,
        'member/return.html',
        {
            "limit": False,
            "loans": loans,
            "home_url": home_url
        })


def book_list(request):
    f = BookFilter(request.GET, queryset=Book.objects.all())
    return render(request, 'core/search-form.html', {'filter': f})

def renew_book(request):
    home_url_list = request.build_absolute_uri().split("/")[:-2]
    home_url = "/".join(home_url_list)
    loans = get_valid_returns(request)
    return render(
        request,
        'member/renew.html',
        {
            "loans": loans,
            "home_url": home_url
        })
        

def renew_successful(request, loan):
    loan_instance = get_object_or_404(Book_Loan, pk=loan)
    today = datetime.date.today()
    limit_date = loan_instance.borrowed_from + datetime.timedelta(days=90)
    extensin_date = today + datetime.timedelta(days=30)
    limit = False
    if extensin_date < limit_date:
        loan_instance.borrowed_to = extensin_date
    else:
        loan_instance.borrowed_to = limit_date
        limit = True
    loan_instance.save()
    return render(request, 'member/renew-successful.html', {'loan': loan_instance, "limit": limit})


def reports_index(request):
    return render(request, 'reports/reports-index.html')

def request_book(request):
    return render(request, 'core/request-book.html')

def bad_members(request):
    all_members = Member.objects.all().prefetch_related('user')
    dictionary = []
    for member in all_members:
        loans = Book_Loan.objects.filter(borrower=member)
        today = datetime.date.today()
        current_loans = [x for x in loans if not x.actual_return_date]
        passed_120 = False
        penalty = 0
        for loan in current_loans:
            if(loan.borrowed_to<today):
                days = today-loan.borrowed_to
                days = days.days
                penalty += days*5
                if days > 120:
                    passed_120 = True
        if (len(loans) > 3 and passed_120):
            dictionary.append({
                'member': member,
                'loans': Book_Loan.objects.filter(borrower=member),
                'penalty': penalty
            })  
    context = {
        'dictionary': dictionary,

    }
    return render(request, 'reports/bad-members.html', context)


def request(request, book):
    book_instance = get_object_or_404(Book, pk=book)
    librarian = Librarian.objects.filter(user=request.user).first()
    home_url_list = request.build_absolute_uri().split("/")[:-2]
    home_url = "/".join(home_url_list)
    # trusted_libraries=["neighborlib@IAU.com", "neighbourlib@KAUST.com"]
    trusted_libraries = ["oafsalem2000@gmail.com"]
    sent = send_mail(
                subject ='KFUPMLIBSYS Book Request',
                message= f'Dear Neghibor Libraries We would like to request the following Book: {book_instance.book_title}, ISBN= {book_instance.ISBN_code} if its available with you, Thanks in advance',
                from_email='kfupmlibsys@yahoo.com',
                recipient_list=trusted_libraries)
    print(f"Succesfully Sent {sent}/{str(len(trusted_libraries))}")
    return render(request, 'core/request.html', {'book': book_instance, "home_url": home_url})