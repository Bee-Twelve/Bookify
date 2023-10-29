from django.urls import path, include
from homepage.views import *
from booklibrary.views import *

app_name = 'booklibrary'

urlpatterns = [
    path('', show_library, name='show_library'),
    path('load-books/', load_books_ajax, name='load_books'),
    path('get-user-bookshelf/', get_user_bookshelf, name='get_user_bookshelf'),
    path('borrow-book/', borrow_book, name='borrow_book'),
    path('complete-reading/', complete_reading, name='complete_reading'),
    path('re-read-book/', re_read_book, name='re_read_book'),
]