from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages 

from .forms import BookForm, CustomUserCreationForm
from .models import Book

import datetime
import json 


def show_homepage(request):
    form = BookForm()
    context = {
            "form":form,
            "last_question": request.session.get('last_login', 'have not submit a question yet')
        }
    return render(request,'homepage.html',context)


@login_required(login_url='/login/')
def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

#Customed Register Function (So it can fill up 'Role' field)
def register(request):
    form = CustomUserCreationForm() #CustomUserCreationForm() imported from forms.py

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('homepage:show_homepage')
    context = {'form':form}
    return render(request, 'register.html', context)

#Default Login Function
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage:show_homepage')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

#Default Logout Function
def logout_user(request):
    logout(request)
    return redirect('homepage:login')

def show_book_review(request):
    # Your view logic here
    context = {
        "form": form,
        "last_question": request.session.get('last_login', 'have not submitted a question yet')
    }
    return render(request, 'bookreview.html', context)
