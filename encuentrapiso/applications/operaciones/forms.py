from django import forms 
from django.contrib.auth.models import User
from .models import *

#Formulario para añadir ofertas, defino las clases TexInput y Select 
#para poder darle formato en los templates. 

class NumberInput(forms.NumberInput):
	input_type: 'number'

class Select(forms.Select):
	input_select="select"

class addOferta(forms.ModelForm):
	class Meta: 
		model=Oferta
		fields=[
			'inmueble',
			'precio',
			'descuento',
			'tipo',
			]

		widgets={
			'inmueble':Select(attrs={'class':'form-control'}),
			'precio':NumberInput(attrs={'class':'form-control'}),
			'descuento':NumberInput( attrs={'class':'form-control'}),
			'tipo':NumberInput( attrs={'class':'form-control'}),				
				}

		labels={
			'inmueble:Inmueble',
			'precio:precio',
			'descuento:descuento',
			'tipo:tipo',
		}
