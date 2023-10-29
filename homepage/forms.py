from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from homepage.models import Book, CustomUser

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['book'].widget.attrs.update({
            'placeholder': 'Enter your books here',
            'cols' : '20',
            'rows' : '5',
        })

#CustomUserCreationForm instead of the default UserCreationForm, so we can add roles to user
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, help_text='Required. Enter your full name.')
    email = forms.EmailField(max_length=255, required=True, help_text='Required. Enter a valid email address.')
    address = forms.CharField(max_length=255, required=True, help_text='Required. Enter your address.')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required. Enter your phone number.')
    birthplace = forms.CharField(max_length=255, required=True, help_text='Required. Enter your birthplace.')
    birthdate = forms.DateField(required=True, help_text='Required. Enter your birthdate (YYYY-MM-DD).')

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'address', 'phone_number', 'birthplace', 'birthdate', 'username', 'password1', 'password2', 'role')

#Same as above, but only to modify
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','role')
