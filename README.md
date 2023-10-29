# Bookify-Web

### Link to our website :  ...

# **Cerita aplikasi yang diajukan serta manfaatnya**
Bookify merupakan website yang kami kembangkan ditujukan kepada kalangan dimulai dari remaja hingga dewasa, dimana mereka bisa mencari, membeli, dan berdiskusi mengenai buku pilihan mereka dengan komunitas yang ada di platform ini. Latar belakang kami untuk meng inisiasi website ini disebabkan oleh sedikitnya persentase masyarakat di Indonesia yang berminat membaca buku. Fakta ini didukung oleh penelitian dari UNESCO yang menyebutkan bahwa Indonesia menempati urutan kedua dari bawah soal literasi dunia, artinya minat baca sangat rendah. Disebutkan juga bahwa persentase minat baca di Indonesia hanya 0.001% artinya hanya 1 dari 1000 orang Indonesia yang memiliki minat baca yang tinggi. Berdasarkan fakta tersebut, kami termotivasi untuk mencoba membangun komunitas baca di Indonesia agar lebih luas lagi dengan mengembangkan website yang memiliki media untuk berdiskusi dan mencari teman yang memiliki interest yang sama di suatu komunitas yang juga memiliki segala sumber informasi mengenai buku dari semua jenis dan genre. Disini para peminat buku juga dapat langsung membeli buku yang mereka minati di BookShop kita yang akan mengarahkan langsung ke website e-commerce yang sesuai. Tetapi tidak hanya itu, apabila mereka belum yakin untuk membelinya langsung, mereka juga dapat mengakses library yang tersedia di website kami untuk meminjam buku (terbatas), jadi mereka dapat tetap membaca dan gabung dalam komunitas di platform kami tanpa mengeluarkan sepeserpun. Untuk fitur pelengkap, kami menambahkan halaman donasi untuk user yang ingin berdonasi ke instansi/sekolah untuk paket up to 50+ buku, bisa berupa buku pelajaran, cerita, dan lain-lain.

**Manfaat Website:**
- Pembeli buku dapat dengan mudah menemukan dan membeli buku melalui toko buku online, sambil melihat ulasan dan peringkat buku.
- Pengguna dapat berinteraksi dan berdiskusi tentang buku, serta mendapatkan pandangan berbeda tentang literatur.
- Memberi refrensi buku bacaan kepada pengguna berdasarkan genre buku favorit pengguna
- Website yang membantu pengguna menemukan buku yang sesuai dengan minat mereka, sehingga meningkatkan kemungkinan mereka membaca lebih banyak dan secara teratur.
- Website yang membantu meningkatkan literasi dan pengetahuan anggota komunitas dengan menyediakan akses mudah ke berbagai buku dan sumber bacaan.
- Sebagai sarana review buku dan sharing buku bagi pengguna
- Pengguna mendapatkan akses ke banyak koleksi buku yang terbagi menjadi berbagai macam genre buku
- Pengguna dapat menyisihkan duitnya untuk berdonasi di halaman "Donasi Buku"

# **Daftar modul yang akan diimplementasikan**
1. *Modul Library:*
Implementasi private library utk user dgn penandaan status "pernah membaca", rekomendasi buku yang cocok utk user, dan bookstore

2. *Modul Book Review & Favorites:*
Supaya user bisa kasih ulasan dan peringkat buku favoritnya.

3. *Modul Literacy Community:*
Pembuatan komunitas sesuai dgn minat bacaan, dengan fitur diskusi

4. *Modul Books Donation:*
Media untuk berdonasi buku yang disalurkan ke sekolah dsb.

5. *Modul Bookmark:*
Filter informasi data buku yg "akan dibaca" oleh user.

# **Sumber dataset katalog buku**
https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata/code (Kaggle)

# **Role atau peran pengguna beserta deskripsinya**

### User Pembaca:
Bisa menambahin buku ke private library, memberi review buku, dan gabung ke komunitas literasi. 

### Admin Komunitas:
Bertanggung jawab mengelola komunitas dan book catalog. Mereka bisa juga dapat memberi rekomendasi buku ke user pembaca.

## TUGAS
- Merancang halaman web
- Mengimplementasikan situs web dengan framework Django dengan memenuhi models, views, dan template
- Memanfaatkan framework CSS untuk mewujudkan responsive web design
- Mengimplementasikan unit test dan deployment (bonus)

## Aturan Khusus per orang dalam membuat models
- Menerapkan models dengan membuat atau memanfaatkan model yang sudah disediakan oleh Django maupun yang sudah dibuat oleh anggota kelompok (pada modul lain).

- Menerapkan views untuk memproses request dan mengolah data untuk menghasilkan respons menggunakan templat HTML maupun mengembalikan respons JSON.

- Menerapkan templat HTML dengan kerangka yang sistematis dan efisien, seperti base.html, header.html, dan footer.html.

- Menerapkan responsive framework pada templat HTML (seperti Bootstrap atau Tailwind).

- Memiliki halaman form yang dapat menerima masukan dari pengguna kemudian diproses oleh views. Contoh pemrosesan oleh views adalah insert data ke dalam model, query data dari model, dan update data pada model.

- Menerapkan JavaScript dengan pemanggilan AJAX.

- Menerapkan filter informasi bagi pengguna yang sudah login saja. Contohnya adalah data alamat, umur, dan nomor ponsel hanya dapat dilihat oleh pengguna yang sudah login saja.

- Menerapkan filter pada dataset katalog buku yang ditampilkan. Contohnya adalah menampilkan daftar buku berdasarkan nama penulisnya.