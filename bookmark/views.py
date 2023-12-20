from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Bookmark
from django.shortcuts import get_object_or_404
from django.urls import reverse
from booklibrary.models import UserBook
from django.contrib import messages
from books.models import Books
import json


@login_required(login_url='/login')
def show_bookmark(request):
    genre = request.GET.get('genre')
    user = request.user
    bookmarks = Books.objects.all()
    if genre:
        bookmarks = bookmarks.filter(book__genre__icontains=genre)
        

    context = {
        'bookmarks': bookmarks,
        'selected_genre': genre,
    }


    return render(request, 'show_bookmark.html', context)



@csrf_exempt
def add_bookmark(request, book_id):
    if request.method == 'POST':
        # Decode the request body to get the JSON data
        data = json.loads(request.body)

        # Extract the relevant information
        forum_id = data.get("forum_id")

        try:
            book = Books.objects.get(id=forum_id)
            user = request.user

            if not Bookmark.objects.filter(user=user, book=book).exists():
                bookmark = Bookmark(user=user, book=book)
                bookmark.save()
                return JsonResponse({"status": "success", "message": f'"{book.title}" telah ditambahkan ke bookmark Anda.'})
            else:
                return JsonResponse({"status": "error", "message": f'"{book.title}" sudah ada di bookmark Anda.'}, status=400)
        except Books.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Buku tidak ditemukan."}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Metode tidak diizinkan"}, status=405)


@csrf_exempt
def delete_bookmark(request, book_id):
    bookmark = get_object_or_404(Bookmark, id=book_id)
    bookmark.delete()

    return HttpResponseRedirect(reverse('bookmark:show_bookmarked'))

def show_json(request):
    data = Bookmark.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")



def show_bookmarked(request):
    genre = request.GET.get('genre')
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)

    if genre:
        bookmarks = Books.objects.filter(book__book__genre=genre)

    context = {
        'bookmarks': bookmarks,
        'selected_genre': genre,
    }

    return render(request, 'show_bookmarked.html', context)

