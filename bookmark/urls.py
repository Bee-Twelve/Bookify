from django.urls import path, include
from homepage.views import *
from bookmark.views import *


app_name = 'bookmark'

urlpatterns = [
    path('', show_bookmark, name='show_bookmark'),
    path('showbookmarked', show_bookmarked, name='show_bookmarked'),
    path('add_bookmark/<int:book_id>/', add_bookmark, name='add_bookmark'),
    path('delete/<int:book_id>/', delete_bookmark, name='delete_bookmark'),
    path('json/', show_json, name='show_json'), 
]
