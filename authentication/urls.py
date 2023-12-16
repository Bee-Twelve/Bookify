from django.urls import path
from authentication.views import login, logout, register, check_is_anonymous
app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('is-anonymous/', check_is_anonymous, name='check_is_anonymous'),
]
