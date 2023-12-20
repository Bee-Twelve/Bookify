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
    book = Books.objects.get(pk=book_id)
    user = request.user
    if not Bookmark.objects.filter(user=user, book=book).exists():
        bookmark = Bookmark(user=user, book=book)
        bookmark.save()
    #     messages.success(request, f'"{book.book.title}" telah ditambahkan ke bookmark Anda.')
    # else:
    #     messages.warning(request, f'"{book.book.title}" sudah ada di bookmark Anda.')  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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

