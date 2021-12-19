from django.http.response import HttpResponse
from django.urls import path, include
from . import views


app_name = "core"

urlpatterns = [
    # path("", views.index, name= "homeIndex"),
    path("register-new-member/", views.register_new_member, name="register-new-member"),
    path("borrow/", views.borrow, name="borrow"),
    path("<str:book_item>/borrowed-successful/", views.borrowed_successful, name="borrowed-successful"),
    path("reserve/", views.reserve, name="reserve"),
    path("<str:book>/reserve-request/",views.reserve_request, name="reserve-request"),
    path("return-book/", views.return_book, name="return-book"),
    path("", views.index, name="home-index"),
    path("register-new-member/", views.register_new_member,name="register-new-member"),
    path("search-form/", views.book_list, name="search-form"),
    path("renew-book/", views.renew_book, name="renew-book"),
    path("<str:loan>/renew-successful/", views.renew_successful, name="renew-successful"),
    path("new-members/", views.report_get_new_members, name="new-members"),
    path("all-members/", views.report_get_all_members, name="all-members"),
    path("reports-index", views.reports_index, name= "reports-index"), 
]
