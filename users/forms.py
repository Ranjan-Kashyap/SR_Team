# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    full_name = forms.CharField(max_length=30, required=True, label='Full Name')
    date_of_birth = forms.DateField(label='Date of Birth')
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("full_name", "email", "date_of_birth", "password1", "password2")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name')
