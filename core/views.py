from django.shortcuts import render
from django.http.response import HttpResponse
from .models import *


def index(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'core/index.html', context)
