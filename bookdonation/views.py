from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .forms import ProductForm
from django.urls import reverse
from .models import Poin

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ProductForm
from django.urls import reverse
from .forms import data_donasi1
from django.http import HttpResponse
from django.core import serializers
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from books.models import Books 
from django.http import JsonResponse





#untuk membuat login form 
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@csrf_exempt
def hapus_produk_ajax(request, product_id):
    try:
        product = get_object_or_404(data_donasi1, pk=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        judul_buku = request.POST.get("judul_buku")
        total_buku = request.POST.get("total_buku")
        resi = request.POST.get("resi")
        user = request.user

        if judul_buku and total_buku:  # Pastikan name dan total_buku tidak kosong
            new_product = data_donasi1(judul_buku=judul_buku, total_buku=total_buku, resi=resi, user=user, status="Menunggu verifikasi")
            new_product.save()

            return JsonResponse({'message': 'Product created successfully'})
            
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_product_json(request):
    product_item = data_donasi1.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', product_item))

def tambah_produk(request, product_id):
    try:
        produk = data_donasi1.objects.get(id=product_id)
        produk.total_buku += 1

        # Validasi agar jumlah produk tidak negatif
        if produk.total_buku < 0:
            produk.total_buku = 0

        produk.save()
        jumlah_item = sum([product.total_buku for product in data_donasi1.objects.all()])

        # Mengembalikan respons JSON yang berisi data jumlah produk yang baru
        return JsonResponse({'new_amount': produk.total_buku, 'new_total_item': jumlah_item})
    
    except data_donasi1.DoesNotExist:
        # Handle jika produk tidak ditemukan
        return JsonResponse({'error': 'Produk tidak ditemukan'}, status=404)

def kurang_produk(request, product_id):
    try:
        produk = data_donasi1.objects.get(id=product_id)
        produk.total_buku -= 1

        # Validasi agar jumlah produk tidak negatif
        if produk.total_buku < 0:
            produk.total_buku = 0

        produk.save()
        jumlah_item = sum([product.total_buku for product in data_donasi1.objects.all()])

        # Mengembalikan respons JSON yang berisi data jumlah produk yang baru
        return JsonResponse({'new_amount': produk.total_buku, 'new_total_item': jumlah_item})
    except data_donasi1.DoesNotExist:
        # Handle jika produk tidak ditemukan
        return JsonResponse({'error': 'Produk tidak ditemukan'}, status=404)
    
def ubah_status(request, product_id):
    try:
        produk = data_donasi1.objects.get(id=product_id)
        produk.status = "Sudah diverifikasi"
        produk.save()

        # Alihkan pengguna kembali ke halaman yang sesuai setelah mengubah status
        return redirect('bookdonation:show_donation')  # Gantilah 'nama_rute_tujuan' dengan nama rute yang sesuai
    except data_donasi1.DoesNotExist:
        # Handle jika produk tidak ditemukan
        return JsonResponse({'error': 'Produk tidak ditemukan'}, status=404)
    


def change_poin(request):
    if request.method == 'POST':
        total_poin_redemption = request.POST.get('total_poin_redemption')

        # Assuming the user is logged in, get the user's Poin object
        user_poin, created = Poin.objects.get_or_create(user=request.user)

        # Update the coin_reedem field
        
        user_poin.coin_reedem += int(total_poin_redemption)
        user_poin.save()

        # Print the total_poin_redemption to the console (optional)
        print("Total Poin Redemption:", total_poin_redemption)

        return JsonResponse({'success': 'Points redeemed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




def hapus_produk(request, product_id):
    try:
        produk = data_donasi1.objects.get(id=product_id)
        produk.delete()
        # Redirect ke halaman yang sesuai setelah menghapus objek
        return redirect('bookdonation:show_donation')
    except data_donasi1.DoesNotExist:
        # Handle jika produk tidak ditemukan
        return redirect('bookdonation:show_donation')  # Redirect ke halaman produk setelah menghapus



def show_json_by_id(request, id):
    data = data_donasi1.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = data_donasi1.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml(request):
    data = data_donasi1.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = data_donasi1.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


    
@login_required(login_url='/login')
def show_donation(request):
    books = Books.objects.all()

    products = data_donasi1.objects.filter(user=request.user)
    item_verif = data_donasi1.objects.filter(status='Sudah diverifikasi', user=request.user)



    semua_produk = data_donasi1.objects.all()
    item_tunggu = data_donasi1.objects.filter(status='Menunggu verifikasi')
    jumlah_item_tunggu = sum(product.total_buku for product in item_tunggu)


    jumlah_item = sum(product.total_buku for product in products)
    jumlah_item_verif = sum(product.total_buku for product in item_verif)
    
    buku_tunggu = jumlah_item - jumlah_item_verif
    user_poin, created = Poin.objects.get_or_create(user=request.user)

    # Accessing coin_reedem
    coin_reedem = user_poin.coin_reedem


    jumlah_poin =jumlah_item_verif * 10 - coin_reedem
    
    

    jumlah_produk = products.count()
    last_login = request.COOKIES.get('last_login', 'Tidak ada informasi login sebelumnya')  # Menggunakan get untuk menghindari KeyError

    context = {
        'name': request.user.username,
        'products': products,
        'jumlah_produk': jumlah_produk,
        'jumlah_item': jumlah_item,
        'jumlah_item_verif': jumlah_item_verif,
        'last_login': last_login,
        'jumlah_poin': jumlah_poin,
        'books' : books,
        'role': request.user.role,
        'semua_produk' : semua_produk,
        'buku_tunggu': buku_tunggu,
        'jumlah_item_tunggu': jumlah_item_tunggu,
        'coin_reedem' : coin_reedem,

    }

    return render(request, "main.html", context)

