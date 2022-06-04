from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class RegistroForm(forms.Form):
	
	dni=forms.CharField(max_length = 9,widget=forms.TextInput(attrs={'class': 'form-control'}))
	nombre= forms.CharField( max_length = 25,widget=forms.TextInput(attrs={'class': 'form-control'}))
	primer_apellido=forms.CharField(max_length = 50,widget=forms.TextInput(attrs={'class': 'form-control'}))
	segundo_apellido=forms.CharField(max_length = 50,widget=forms.TextInput(attrs={'class': 'form-control'}))
	telefono=forms.CharField(max_length=9,widget=forms.TextInput(attrs={'class': 'form-control'}))


class CreacionUser(UserCreationForm):
	
	username=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'class': 'form-control'}))


	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')  
		cliente = models.OneToOneField(User, on_delete=models.CASCADE)


