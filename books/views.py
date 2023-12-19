from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from books.models import Books

# Create your views here.
def get_books(request):
    data = Books.objects.all()
    return HttpResponse(serializers.serialize("json", data),
    content_type = "application/json")


def fetch_book(request):
    if request.method == 'GET':
        data = Books.objects.all().order_by('pk')
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def search_books(request):
    query = request.GET.get('q', '')
    if (query == ''):
        data = Books.objects.all().order_by('pk')
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    else:
        data = Books.objects.filter(
            title__contains=query).order_by('pk') | Books.objects.filter(author__contains=query).order_by('pk') | Books.objects.filter(genre__contains=query).order_by('pk')
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
