from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from homepage.models import CustomUser
from books.models import Books
#-------------------------------------IMPORTANT!---------------------------------------------------
# ALWAYS USE 'settings.AUTH_USER_MODEL' INSTEAD OF THE USUAL 'User' WHEN CONNECTING MODELS TO USER!
# i.e. user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#                    OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#                    ManyToManyField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

# NOT THIS -> models.ForeignKey(User,on_delete=models.CASCADE)

# BECAUSE WE ARE USING CUSTOM USER
#--------------------------------------------------------------------------------------------------
# Create your models here.

class UserBook(models.Model):
    READING_STATUS = (
        ('not_started', 'Not Started'),
        ('reading', 'Currently Reading'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=12, choices=READING_STATUS, default='not_started')
    start_date = models.DateField(null=True, blank=True)  # when the user started reading
    end_date = models.DateField(null=True, blank=True)  # when the user finished reading