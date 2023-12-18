"""
URL configuration for bookify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from bookreview.views import homepage  # Pastikan Anda mengimpor 'homepage' dengan benar

urlpatterns = [
    # path('', homepage, name='homepage'),  # Tambahkan path untuk halaman beranda
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('booklibrary/', include('booklibrary.urls')),
    path('bookreview/', include('bookreview.urls')), #Path bookreview diubah dari 'book/' menjadi 'bookreview/'
    path('bookcommunity/', include('bookcommunity.urls')),
    path('bookdonation/', include('bookdonation.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('api/books/', include('books.urls')),
    path('authentication/', include('authentication.urls')), 
]
