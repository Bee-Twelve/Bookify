from datetime import timezone
import json
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from books.models import Books
from booklibrary.models import UserBook

# Create your views here.
# MAIN PAGE
def show_library(request):
    return render(request, 'library.html')

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

# SHOW USER'S BOOKSHELF
@login_required
def get_user_bookshelf(request):
    user = request.user
    user_books = UserBook.objects.filter(user=request.user)

    books_data = []

    for user_book in user_books:
        book = user_book.book
        books_data.append({
            'id' : book.id,
            'title': book.title,
            'author': book.author,
            'published_year': book.published_year,
            'genre': book.genre,
            'pages' : book.pages,
            'description': book.description,
            'thumbnail': book.thumbnail,
            'ratings_avg': book.ratings_avg,
            'ratings_count': book.ratings_count,
            'isbn10': book.isbn10,
            'isbn13': book.isbn13,
            'status': user_book.get_status_display()
        })

    return JsonResponse(books_data, safe=False)

from django.http import JsonResponse

# BORROW BOOK
def borrow_book(request):
    if request.method == 'POST':
        user = request.user
        book_id = request.POST.get('book_id')
        book = Books.objects.get(id=book_id)

        # Create or get a UserBook instance
        user_book, created = UserBook.objects.get_or_create(user=user, book=book)

        if created:
            user_book.status = 'reading'
            user_book.save()

            return JsonResponse({'status': 'success', 'message': 'Book added to shelf successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Book is already in your shelf!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

# COMPLETE READING
@csrf_exempt
def complete_reading(request):
    if request.method == 'POST':
        user = request.user
        book_id = request.POST.get('book_id')
        book = Books.objects.get(id=book_id)

        # Get a UserBook instance
        user_book = UserBook.objects.filter(user=user, book=book).first()

        if user_book:
            user_book.status = 'completed'
            user_book.save()
            return JsonResponse({'status': 'success', 'message': 'Status updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Book is not in your shelf!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
# REREADING BOOK
@csrf_exempt
def re_read_book(request):
    if request.method == 'POST':
        user = request.user
        book_id = request.POST.get('book_id')
        book = Books.objects.get(id=book_id)

        # Get a UserBook instance
        user_book = UserBook.objects.filter(user=user, book=book).first()

        if user_book:
            user_book.status = 'reading'
            user_book.save()

            return JsonResponse({'status': 'success', 'message': 'Book status updated to currently reading!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Book not found in your shelf!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
@csrf_exempt
def add_to_bookshelf(request):
    if request.method == 'POST':
        # Get the book ID from the POST data
        book_id = request.POST.get('book_id')

        # Make sure the book ID is provided
        if not book_id:
            return JsonResponse({'status': 'error', 'message': 'Book ID is required.'}, status=400)

        # Try to get the book from the database
        try:
            book = Books.objects.get(id=book_id)
        except Books.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book does not exist.'}, status=404)

        # Check if the book is already in the user's bookshelf
        user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)

        # If the book was added to the bookshelf (i.e., it didn't exist before)
        if created:
            user_book.status = 'reading'
            user_book.save()
            return JsonResponse({'status': 'success', 'message': 'Book added to your bookshelf.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Book is already on your bookshelf.'})

    # If it's not a POST request, return an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@login_required
@csrf_exempt
def show_bookshelf(request):
    if request.method == 'GET':
        user_books = UserBook.objects.filter(user=request.user)
        books_data = []

        for user_book in user_books:
            book = user_book.book
            books_data.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'published_year': book.published_year,
                'genre': book.genre,
                'pages': book.pages,
                'description': book.description,
                'thumbnail': book.thumbnail,
                'ratings_avg': book.ratings_avg,
                'ratings_count': book.ratings_count,
                'isbn10': book.isbn10,
                'isbn13': book.isbn13,
                'status': user_book.get_status_display(),
            })

        return HttpResponse(json.dumps(books_data), content_type="application/json")

    return HttpResponse(
        json.dumps({'status': 'error', 'message': 'Invalid request method.'}),
        content_type="application/json",
        status=405
    )

@login_required
@csrf_exempt
def search_user_books(request):
    user = request.user
    query = request.GET.get('q', '')

    if not user.is_authenticated:
        return HttpResponse(
            json.dumps({'status': 'error', 'message': 'User not authenticated'}),
            content_type="application/json", status=401
        )

    if query == '':
        user_books = UserBook.objects.filter(user=user)
    else:
        user_books = UserBook.objects.filter(
            Q(book__title__icontains=query) | 
            Q(book__author__icontains=query) | 
            Q(book__genre__iexact=query),
            user=user
        )

    books_data = [{
        'id': user_book.book.id,
        'title': user_book.book.title,
        'author': user_book.book.author,
        'published_year': user_book.book.published_year,
        'genre': user_book.book.genre,
        'pages': user_book.book.pages,
        'description': user_book.book.description,
        'thumbnail': user_book.book.thumbnail,
        'ratings_avg': user_book.book.ratings_avg,
        'ratings_count': user_book.book.ratings_count,
        'isbn10': user_book.book.isbn10,
        'isbn13': user_book.book.isbn13,
        'status': user_book.get_status_display(),
    } for user_book in user_books]

    return HttpResponse(json.dumps(books_data), content_type="application/json")

def show_userbook(request):
    user_books = UserBook.objects.all()  # Adjust the query as needed

    data = [{
        'id': book.book.id,
        'title': book.book.title,
        'author': book.book.author,
        'published_year': book.book.published_year,
        'genre': book.book.genre,
        'pages': book.book.pages,
        'description': book.book.description,
        'thumbnail': book.book.thumbnail,
        'ratings_avg': book.book.ratings_avg,
        'ratings_count': book.book.ratings_count,
        'isbn10': book.book.isbn10,
        'isbn13': book.book.isbn13,
        'status': book.get_status_display(),
    } for book in user_books]
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def update_reading_status(request, book_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

    if request.method == 'POST':
        # Fetch the UserBook instance
        user_book = get_object_or_404(UserBook, user=user, book_id=book_id)

        # Update the status and end_date
        user_book.status = 'completed'
        user_book.end_date = timezone.now().date()
        user_book.save()

        return JsonResponse({'status': 'success', 'message': 'Reading status updated to completed.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)