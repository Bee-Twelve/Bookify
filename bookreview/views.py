from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Func
from books.models import Books
from django.db.models import Q

# Create your views here.
def book_review(request, book_id):
    book = get_object_or_404(Books, isbn13=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'bookreview.html', {'book': book, 'reviews': reviews})

@login_required
def favorite_books(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    return render(request, 'bookreview/favorite_books.html', {'favorites': favorites})

def show_library(request):
    return render(request, 'books.html')

@csrf_exempt
def load_books_ajax(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')  # Ambil kata kunci pencarian dari permintaan POST

        # Ambil buku dari basis data
        if search_query:
            books = Books.objects.filter(Q(title__icontains=search_query) | Q(isbn10__icontains=search_query) | Q(isbn13__icontains=search_query))
        else:
            books = Books.objects.all()

        # Serialisasi data buku ke dalam format JSON
        serialized_books = serializers.serialize('json', books)

        # Kirim data buku sebagai respons JSON
        return JsonResponse({'status': 'success', 'books': serialized_books})

    # Jika metode permintaan tidak valid
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@csrf_exempt
def load_favorites_books_ajax(request) :
    # Mendapatkan daftar buku favorit dari pengguna yang sedang login
    favorites = Favorite.objects.filter(user=request.user)
    
    # Mengambil nilai book dari objek Favorite
    favorite_books = [favorite.book for favorite in favorites]
        
    # Serialisasi data buku ke dalam format JSON
    serialized_favorites = serializers.serialize('json', favorite_books)

    # Kirim data buku favorit sebagai respons JSON
    return JsonResponse({'status': 'success', 'favorites': serialized_favorites})

@login_required
@csrf_exempt
def add_favorite_ajax(request, book_id):
    try:
        book = Books.objects.get(pk=book_id)
        # Cek apakah buku sudah ada dalam favorit pengguna
        existing_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
        if not existing_favorite:
            # Jika buku belum ada dalam favorit, tambahkan ke favorit pengguna
            favorite = Favorite(user=request.user, book=book)
            favorite.save()
            return JsonResponse({'status': 'success', 'message': 'Buku berhasil ditambahkan ke favorit.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Buku sudah ada dalam favorit.'})
    except Books.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Buku tidak ditemukan.'}, status=404)

@login_required
@csrf_exempt
def remove_favorite_ajax(request, book_id):
    try:
        book = Books.objects.get(pk=book_id)
        # Hapus buku dari favorit pengguna jika ada
        favorite = Favorite.objects.filter(user=request.user, book=book).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'success', 'message': 'Buku berhasil dihapus dari favorit.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Buku tidak ada dalam favorit.'})
    except Books.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Buku tidak ditemukan.'}, status=404)
    
"""
Fungsi ini memperbarui ratings_count dan ratings_avg pada objek Books
berdasarkan perubahan rating dari review.
"""
def update_book_ratings(book, new_rating, old_rating=None, action='add'):
    if action == 'update' and old_rating is not None:
        # Menghitung ulang ratings_avg jika nilai rating berubah saat update
        book.ratings_avg = (F('ratings_avg') * F('ratings_count') - old_rating + new_rating) / F('ratings_count')
    elif action == 'delete':
        # Mengurangi 1 dari ratings_count dan menghitung ulang ratings_avg saat delete
        if book.ratings_count > 0:
            book.ratings_avg = (F('ratings_avg') * F('ratings_count') - new_rating) / (F('ratings_count') - 1)
        else:
            book.ratings_avg = 0
        book.ratings_count = F('ratings_count') - 1
    else:
        # Menambah 1 ke ratings_count dan menghitung ulang ratings_avg saat add
        book.ratings_avg = (F('ratings_avg') * F('ratings_count') + new_rating) / (F('ratings_count') + 1)
        book.ratings_count = F('ratings_count') + 1
    
    # Memanggil fungsi round() sebelum nilai ratings_avg disimpan
    book.ratings_avg = Func(F('ratings_avg'), function='ROUND', template='%(function)s(%(expressions)s, 2)')
    
    book.save()

@login_required
@csrf_exempt
def ajax_add_review(request, book_id):
    response_data = {}
    
    book = Books.objects.get(isbn13=book_id)
    
    if Review.objects.filter(book=book, user=request.user).exists():
        response_data = {'status': 'error', 'code': 400, 'message': 'Anda sudah mereview buku ini'}
    else:
        if request.method == 'POST':
            rating = request.POST.get('book_rating')
            comment = request.POST.get('book_review')
            user = request.user
            review = Review(book=book, user=user, rating=rating, comment=comment)
            review.save()
            
            # Memanggil fungsi update_book_ratings untuk mengupdate ratings_count dan ratings_avg
            update_book_ratings(book, rating, action='add')
                
            response_data = {'status': 'success', 'code': 200, 'message': "Review berhasil ditambahkan."}
    
    return JsonResponse(response_data)

@login_required
@csrf_exempt
def ajax_update_review(request, review_id):
    response_data = {}
    
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = request.POST.get('book_rating')
        comment = request.POST.get('book_review')
        
        # Memanggil fungsi update_book_ratings untuk mengupdate ratings_count dan ratings_avg
        update_book_ratings(review.book, rating, review.rating, action='update')
        
        review.rating = rating
        review.comment = comment
        review.save()
        response_data = {'status': 'success', 'code': 200, 'message': "Review berhasil diedit."}

    return JsonResponse(response_data)

@login_required
@require_POST
@csrf_exempt
def ajax_delete_review(request, review_id):
    response_data = {}
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    # Memanggil fungsi update_book_ratings untuk mengupdate ratings_count dan ratings_avg
    update_book_ratings(review.book, review.rating, action='delete')
    
    if review.delete() :
        response_data = {'status': 'success', 'code': 200, 'message': "Review berhasil dihapus."}
    return JsonResponse(response_data)
        