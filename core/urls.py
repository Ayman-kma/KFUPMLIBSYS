from django.http.response import HttpResponse
from django.urls import path, include
from . import views


app_name = "core"

urlpatterns = [
    path("", views.index, name= "home-index"),
]