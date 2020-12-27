from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# User model with extra fields
class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
        label='First Name', help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
        label='Last Name', help_text='Optional.')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
        'first_name', 'last_name']

# Show Login Form
class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']