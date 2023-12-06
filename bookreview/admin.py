from django.contrib import admin
from .models import Review, Favorite

# Register your models here.
admin.site.register(Review)
admin.site.register(Favorite)