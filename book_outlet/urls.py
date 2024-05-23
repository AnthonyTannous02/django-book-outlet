from django.urls import path
from . import views

urlpatterns = [
    path("all-books", views.all_books, name="all-books"),
    path("book-detail/<slug:slug>", views.book_detail, name="book-detail"),
]
