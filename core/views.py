from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def Index(request):
    d = {
        "Names": ["Osama", "Ayman", "Omran"],
        "text": "this is a text"
    }
    return render(request, "index.html", d)

def About(request):
    return HttpResponse("About")