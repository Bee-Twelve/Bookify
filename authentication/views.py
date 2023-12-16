from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from homepage.forms import CustomUserCreationForm
import json

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Create a form instance and populate it with data from the request
        form = CustomUserCreationForm(data)

        # Check whether the form is valid
        if form.is_valid():
            # If valid, save the new user
            form.save()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # If the form is invalid, return the error messages
            return JsonResponse({'status': 'failed', 'errors': form.errors}, status=400)

    else:
        return JsonResponse({'status': 'error'}, status=401)

def check_is_anonymous(request):
  print(request.user.is_anonymous)
  return JsonResponse({
      "anonymous": request.user.is_anonymous
  }, status=200)
