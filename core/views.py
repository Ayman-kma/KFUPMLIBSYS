from django.shortcuts import render
from django.http.response import HttpResponse
from .models import *
from .filters import BookFilter
from django.views.generic import ListView

def index(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'core/index.html', context)


def register_new_member(request):
    context = {}
    return render(request, 'core/register-new-member.html', context)




def book_list(request):
    f = BookFilter(request.GET, queryset=Book.objects.all())
    return render(request, 'core/search-form.html', {'filter': f})