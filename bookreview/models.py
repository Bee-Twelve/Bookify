from django.db import models
from books.models import Books
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
class Review(models.Model):
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

class Favorite(models.Model):
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
