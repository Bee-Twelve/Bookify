from django.urls import path, include
from books.views import *
app_name = 'books'

urlpatterns = [
    path("", get_books, name="get_books"),
    path("fetch-book/", fetch_book, name='fetch_book'),
    path('search/', search_books, name='search_books'),
]