from django.forms import ModelForm
from .models import data_donasi1

class ProductForm(ModelForm):
    class Meta:
        model = data_donasi1
        fields = ["judul_buku", "total_buku", "resi", "status"]