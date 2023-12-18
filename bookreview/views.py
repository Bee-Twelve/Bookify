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
import json

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

@csrf_exempt
@login_required
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


def book_review_api(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    reviews = Review.objects.filter(book=book)

    # Create a dictionary to represent the JSON response
    response_data = {
        'book': {
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'pages': book.pages,
            'published_year': book.published_year,
            'description': book.description,
            'thumbnail': book.thumbnail,
            'ratings_avg': book.ratings_avg,
            'ratings_count': book.ratings_count,
            'isbn10': book.isbn10,
            'isbn13': book.isbn13,
        },
        'reviews': [
            {
                'user': review.user.username,
                'comment': review.comment,
                'rating': review.rating,
            }
            for review in reviews
        ],
    }

    return JsonResponse(response_data)


@csrf_exempt
def load_books_all(request):
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
        return HttpResponse(serialized_books, content_type = "application/json")

    # Jika metode permintaan tidak valid
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



@login_required(login_url='/login/')
@csrf_exempt
def add_review_api(request, book_id):
    response_data = {'status': 'success', 'code': 123, 'message': "haha oke"}
    book = Books.objects.get(isbn13=book_id)
    if request.user.is_authenticated == False:
        response_data = {'status': 'error', 'code': 401, 'message': 'Anda harus login untuk menambahkan buku ke favorit.'}
        return JsonResponse(response_data, content_type="application/json")
    else:
        if Review.objects.filter(book=book, user=request.user).exists():
            response_data = {'status': 'error', 'code': 400, 'message': 'Anda sudah mereview buku ini'}
        else:
            if request.method == 'POST':
                rating = request.POST.get('book_rating')
                print(f"rating: {rating}, tipe: {type(rating)}")
                comment = request.POST.get('book_review')
                print(f"comment: {comment}, tipe: {type(comment)}")
                user = request.user
                review = Review(book=book, user=user, rating=rating, comment=comment)
                review.save()
                
                # Memanggil fungsi update_book_ratings untuk mengupdate ratings_count dan ratings_avg
                update_book_ratings(book, rating, action='add')
                    
                response_data = {'status': 'success', 'code': 200, 'message': "Review berhasil ditambahkan."}
        
        return JsonResponse(response_data, content_type = "application/json")



# @login_required(login_url='/login/')
# @csrf_exempt
# def add_review_api(request, book_id):
#     response_data = {}

#     if request.user.is_authenticated == False:
#         response_data = {'status': 'error', 'code': 401, 'message': 'Anda harus login untuk menambahkan review.'}
#         return JsonResponse(response_data, content_type="application/json")
#     else: 
#         book = get_object_or_404(Books, pk=book_id)
#         user = request.user
#         if Review.objects.filter(book=book, user=request.user).exists():
#             response_data = {'status': 'error', 'code': 400, 'message': 'Anda sudah mereview buku ini'}
#         else:
#             if request.method == 'POST':
#                 data = json.loads(request.body)
#                 print(data)
#                 review = Review.objects.create(
#                     book = book,
#                     rating = int(data['book_rating']),
#                     comment = data['book_review'],
#                     user = User.objects.get(username=data["username"]),
#                     review = Review(book=book, user=user, rating=rating, comment=comment)
#                 )
#                 review.save()
#                 update_book_ratings(book, rating, action='add')

#                 response_data = {'status': 'success', 'code': 200, 'message': "Review berhasil ditambahkan."}

#             else:
#                 return JsonResponse({"status": "Not Found"}, status=404)
#     return JsonResponse(response_data, content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def load_favorites_books_api(request):
    if request.user.is_authenticated == False:
        response_data = {'status': 'error', 'code': 401, 'message': 'Anda harus login untuk melihat daftar buku favorit'}
        return JsonResponse(response_data, content_type="application/json")
    else:
        # Mendapatkan daftar buku favorit dari pengguna yang sedang login
        favorites = Favorite.objects.filter(user=request.user)
        
        favorite_books = [
            {
                "pk": favorite.book.pk,
                "fields": {
                    "title": favorite.book.title,
                    "author": favorite.book.author,
                    "genre": favorite.book.genre,
                    "pages": favorite.book.pages,
                    "published_year": favorite.book.published_year,
                    "description": favorite.book.description,
                    "thumbnail": favorite.book.thumbnail,
                    "ratings_avg": favorite.book.ratings_avg,
                    "ratings_count": favorite.book.ratings_count,
                    "isbn10": favorite.book.isbn10,
                    "isbn13": favorite.book.isbn13,
                }
            }
            for favorite in favorites
        ]
        
        # bagian response data
        response_data = {
            'status': 'success', 
            'code': 200, 
            'message': 'Daftar buku favorit berhasil dimuat', 
            'data': favorite_books
        }
        return JsonResponse(response_data, content_type="application/json")


@csrf_exempt
def add_favorite_api(request, book_id):
    response_data = {}
    
    if request.user.is_authenticated == False:
        response_data = {'status': 'error', 'code': 401, 'message': 'Anda harus login untuk menambahkan buku ke favorit.'}
        return JsonResponse(response_data, content_type="application/json")
    else:
        try:
            book = get_object_or_404(Books, pk=book_id)
            # Check if the book is already in the user's favorites
            existing_favorite = Favorite.objects.filter(user=request.POST.get('user'), book=book).exists()
            if not existing_favorite:
                # If the book is not in favorites, add it to the user's favorites
                favorite = Favorite(user=request.user, book=book)
                favorite.save()
                response_data = {'status': 'success', 'message': 'Buku berhasil ditambahkan ke favorit.'}
            else:
                response_data = {'status': 'error', 'message': 'Buku sudah ada dalam favorit.'}
        except Books.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Buku tidak ditemukan.'}

    # Return the serialized data as a JSON response
    return JsonResponse(response_data, content_type="application/json")


@csrf_exempt
def remove_favorite_api(request, book_id):
    response_data = {}

    if request.user.is_authenticated == False:
        response_data = {'status': 'error', 'message': 'Anda harus login untuk menghapus buku dari favorit.'}
        return JsonResponse(response_data, content_type="application/json")
    else:
        try:
            book = get_object_or_404(Books, pk=book_id)
            # Remove the book from the user's favorites if it exists
            favorite = Favorite.objects.filter(user=request.user, book=book).first()
            if favorite:
                favorite.delete()
                response_data = {'status': 'success', 'message': 'Buku berhasil dihapus dari favorit.'}
            else:
                response_data = {'status': 'error', 'message': 'Buku tidak ada dalam favorit.'}
        except Books.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Buku tidak ditemukan.'}

    # Return the serialized data as a JSON response
    return JsonResponse(response_data, content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def api_update_review(request, review_id):
    response_data = {}

    if request.user.is_authenticated == False:
        response_data = {'status': 'error', 'code': 401, 'message': 'Anda harus login untuk update review buku Anda.'}
        return JsonResponse(response_data, content_type="application/json")
    else:
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

    return JsonResponse(response_data, content_type="application/json")
