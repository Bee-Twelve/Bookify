from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from books.models import Books
import json
from .models import *
from .forms import *

# Create your views here.
def show_community(request):
    forums=Forum.objects.all()
    count = Forum.objects.count()
    books = Books.objects.all()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
             'count':count,
             'books':books,
              'discussions':discussions}
    
    return render(request,'home.html',context)


def get_forums_and_discussions(request):
    forums = Forum.objects.all()
    discussions = Discussion.objects.all()
    
    # Serialize forums and discussions
    forums_data = []
    for forum in forums:
        forum_data = {
            'book': forum.book,
            'subject': forum.subject,
            'description': forum.description,
            'user': {
                'username': forum.user.username,
                'id':forum.id,
                'date_created':forum.date_created,
                'isloggedin':request.user.username==forum.user.username,
                # Add other user-related fields as needed
            }
        }
        forums_data.append(forum_data)

    discussions_data = []
    for discussion in discussions:
        discussion_data = {
            'forum':discussion.forum.id,
            'discuss': discussion.discuss,
            'user': {
                'username': discussion.user.username,
                # Add other user-related fields as needed
            },
            # Include discussion data as needed
        }
        discussions_data.append(discussion_data)

    data = {
        'forums': forums_data,
        'discussions': discussions_data,
    }

    return JsonResponse(data)

@csrf_exempt
@login_required
def add_discussion_ajax(request):
    if request.method == 'POST':
        forum_id = request.POST.get("forum_id")
        discuss = request.POST.get("discuss")
        user = request.user

        forum = Forum.objects.get(pk=forum_id)

        new_discussion = Discussion(forum=forum, discuss=discuss, user=user)
        new_discussion.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
@login_required
def add_product_ajax(request):
    if request.method == 'POST':
        book = request.POST.get("book")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        user = request.user

        new_forum = Forum(book=book, subject=subject, description=description, user=user)
        new_forum.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
@login_required
def delete_forum_ajax(request, forum_id):
    if request.method == 'DELETE':
        forum = Forum.objects.get(pk=forum_id)
        forum.delete()
        return JsonResponse({'message': 'Forum deleted successfully'})
    return HttpResponseNotFound()

def show_json_forum(request):
    forums = Forum.objects.all()
    forums_data = []

    for forum in forums:
        forums_data.append({
            'model': 'bookcommunity.forum',
            'pk': forum.pk,
            'fields': {
                'user': forum.user.username,  # assuming the User model has a username field
                'book': forum.book,
                'subject': forum.subject,
                'description': forum.description,
                'date_created': forum.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            }
        })

    return JsonResponse(forums_data, safe=False)

       
def show_json_discussion(request):
    discussions = Discussion.objects.all()
    discussions_data = []

    for discussion in discussions:
        discussions_data.append({
            'model': 'bookcommunity.discussion',
            'pk': discussion.pk,
            'fields': {
                'user': discussion.user.username if discussion.user else None,
                'forum': discussion.forum.pk,
                'discuss': discussion.discuss,
            }
        })

    return JsonResponse(discussions_data, safe=False)




@csrf_exempt
def create_forum_flutter(request):
    # Check if the user is not authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User not logged in"}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)

        new_forum = Forum.objects.create(
            user=request.user,
            book=data["book"],
            subject=data["subject"],
            description=data["description"]
        )

        new_forum.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    

@csrf_exempt
def create_discussion_flutter(request):
    # Check if the user is not authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User not logged in"}, status=401)

    if request.method == 'POST':
        # Decode the request body to get the JSON data
        data = json.loads(request.body)

        # Extract the relevant information
        forum_id = data.get("forum_id")
        discuss = data.get("discuss")

        try:
            # Retrieve the Forum object by its ID
            forum = Forum.objects.get(pk=forum_id)

            # Create and save the new Discussion object
            new_discussion = Discussion(forum=forum, discuss=discuss, user=request.user)
            new_discussion.save()

            # Return a success response
            return JsonResponse({"status": "success"}, status=201)

        except Forum.DoesNotExist:
            # Return an error response if the forum is not found
            return JsonResponse({"status": "error", "message": "Forum not found"}, status=404)

    # Return an error response for non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
