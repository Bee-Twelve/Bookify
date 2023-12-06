from django.test import TestCase
from django.contrib.auth.models import User 

from django.test import TestCase
from django.urls import reverse
from .models import data_donasi1  # Sesuaikan dengan model Anda

class MyViewsTest(TestCase):
    def setUp(self):
        # Persiapan data yang diperlukan untuk pengujian
        self.user = User.objects.create(username="testuser")
        self.product = data_donasi1.objects.create(
            judul_buku="Test Book",
            total_buku=5,
            resi="12345",
            status="menunggu verifikasi",
            user=self.user,
        )

    def test_add_product_ajax(self):
        # Pengujian view 'add_product_ajax'
        url = reverse("nama_rute_add_product_ajax")  # Ganti 'nama_rute_add_product_ajax' dengan nama rute yang sesuai
        data = {
            "judul_buku": "New Book",
            "total_buku": 10,
            "resi": "67890",
            "status": "menunggu verifikasi",
        }
        self.client.force_login(self.user)  # Masukkan pengguna yang telah login
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)  # Periksa apakah responsnya sesuai dengan yang diharapkan

        # Periksa apakah produk baru telah dibuat di database
        new_product = data_donasi1.objects.get(judul_buku="New Book")
        self.assertEqual(new_product.total_buku, 10)

    def test_tambah_produk(self):
        # Pengujian view 'tambah_produk'
        url = reverse("nama_rute_tambah_produk", args=[self.product.id])  # Ganti 'nama_rute_tambah_produk' dengan nama rute yang sesuai
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Periksa apakah responsnya sesuai dengan yang diharapkan

        # Periksa apakah jumlah produk telah bertambah
        updated_product = data_donasi1.objects.get(id=self.product.id)
        self.assertEqual(updated_product.total_buku, 6)

    # Tambahkan pengujian untuk view-view lain sesuai kebutuhan Anda

