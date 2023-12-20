from django.urls import path, include
from homepage.views import *
from bookdonation.views import *

app_name = 'bookdonation'

urlpatterns = [
    path('', show_donation, name='show_donation'),
   
    path('xml/', show_xml, name='show_xml'), 
    path('json/', show_json, name='show_json'), 
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('ubah_status/<int:product_id>/', ubah_status, name='ubah_status'),
    path('change_poin/', change_poin, name='change_poin'),
    path('hapus_produk/<int:product_id>/', hapus_produk, name='hapus_produk'),
    path('tambah_produk/<int:product_id>/', tambah_produk, name='tambah_produk'),
    path('kurang_produk/<int:product_id>/', kurang_produk, name='kurang_produk'),
    path('get-product/', get_product_json, name='get_product_json'),
    path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('hapus_produk_ajax/<int:product_id>/', hapus_produk_ajax, name='hapus_produk_ajax')
    
]