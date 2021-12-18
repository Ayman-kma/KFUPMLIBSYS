from django.http.response import HttpResponse
from django.urls import path, include
from . import views


app_name = "core"

urlpatterns = [
    path("", views.index, name= "home-index"),
    path("register-new-member/", views.register_new_member, name= "register-new-member"),
    path("search-form/", views.book_list, name= "search-form"),
]