from django.urls import path
from . import views

app_name = 'bookreview'

urlpatterns = [
    path('', views.show_library, name='show_library'),
    path('book/<int:book_id>/review/', views.book_review, name='book_review'),
    path('book/<int:book_id>/add_review/', views.ajax_add_review, name='add_review'),
    path('book/update_review/<int:review_id>', views.ajax_update_review, name='update_review'),
    path('book/delete_review/<int:review_id>', views.ajax_delete_review, name='delete_review'),
    path('favorites/', views.favorite_books, name='favorite_books'),
    path('load-books/', views.load_books_ajax, name='load_books'),
    path('load-favorites/', views.load_favorites_books_ajax, name='load_favorites'),
    path('add-favorite/<int:book_id>/', views.add_favorite_ajax, name='add_favorite'),
    path('remove-favorite/<int:book_id>/', views.remove_favorite_ajax, name='remove_favorite'),
]
