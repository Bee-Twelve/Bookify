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
    path('book/load-books-json/<int:book_id>/', views.book_review_api, name='load_books_json'),
    path('load-books-all/', views.load_books_all, name='load_books_all'),
    path('load-favorites-api/', views.load_favorites_books_api, name='load_favorites_api'),
    path('book/<int:book_id>/add_review_api/', views.add_review_api, name='add_review_api'),
    path('remove-favorite-api/<int:book_id>/', views.remove_favorite_api, name='remove_favorite_api'),
    path('add-favorite-api/<int:book_id>/', views.add_favorite_api, name='add_favorite_api'),
    path('book/api_update_review/<int:review_id>', views.api_update_review, name='api_update_review'),

]