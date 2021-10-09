from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewAccountForm(UserCreationForm):
    email = forms.CharField(max_length=200, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
