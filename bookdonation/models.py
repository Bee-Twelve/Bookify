from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#-------------------------------------IMPORTANT!---------------------------------------------------
# ALWAYS USE 'settings.AUTH_USER_MODEL' INSTEAD OF THE USUAL 'User' WHEN CONNECTING MODELS TO USER!
# i.e. user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#                    OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#                    ManyToManyField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

# NOT THIS -> models.ForeignKey(User,on_delete=models.CASCADE)

# BECAUSE WE ARE USING CUSTOM USER
#--------------------------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User


class data_donasi1(models.Model):
    judul_buku = models.CharField(max_length=255)
    total_buku = models.IntegerField()
    resi = models.TextField()
    status = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Poin(models.Model):
    coin_reedem = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)