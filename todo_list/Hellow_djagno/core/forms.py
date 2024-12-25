from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUp(UserCreationForm):
    password1 = forms.CharField(label='Password',
     widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password',
     widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(label="Emial", widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    class Meta:
        model = User
        fields = ['username', 'email','password1',  'password2']
        labels = {'email':'Email'}
        widegts = {'username':forms.TextInput(attrs={'class':'form-control'})}


class Login(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', 
            widget=forms.PasswordInput(attrs={'class':'form-control'}))