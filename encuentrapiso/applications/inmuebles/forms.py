from django import forms 
from django.contrib.auth.models import User
from .models import *

#Formulario para añadir inmuebles, defino las clases TexArea, TexInput y Select 
#para poder darle formato en los templates. 

class TexArea(forms.Textarea):
	input_type="texarea"

class TexInput(forms.TextInput):
	input_text="texinput"

class Select(forms.Select):
	input_select="select"

class addInmueble(forms.ModelForm):
	class Meta: 
		model=Inmueble
		fields=[
			'propietario',
			'direccion',
			'localizacion',
			'codigo_postal',
			'metros',
			'habitacion',
			'planta',
			'wc',
			'orientacion',
			'construccion',
			'comunidad',
			'ascensor',
			'terraza',
			'patio',
			'observacion',
			'imagenPrincipal',
			'imagen1',
			'imagen2',
			'imagen3',
			'imagen4',
			]

		widgets={
				'propietario':Select(attrs={'class':'form-control'}),
				'localizacion':Select(attrs={'class':'form-control'}),
				'observacion':TexArea(attrs={'class':'form-control','rows':'10','cols':'5'}),
				'direccion':TexInput(attrs={'class':'form-control'}),
				'codigo_postal':TexInput( attrs={'class':'form-control'}),
				'construccion':TexInput( attrs={'class':'form-control'}),
				'metros':TexInput( attrs={'class':'form-control'}),
				'habitacion':Select(attrs={'class':'form-control'}),
				'planta':TexInput( attrs={'class':'form-control'}),
				'wc':TexInput( attrs={'class':'form-control'}),
				'orientacion':Select(attrs={'class':'form-control'}),
				'comunidad':TexInput( attrs={'class':'form-control'}),

				
				}

		labels={
			'propietario:Propietario',
			'direccion:Dirección',
			'localizacion:Localización',
			'codigo_postal:Código Postal',
			'metros: Metros',
			'habitacion: Habitaciones',
			'planta:Planta',
			'wc: Baños',
			'orientacion: Orientación',
			'construccion: Año Construccion',
			'comunidad: Precio de Comunidad',
			'ascensor: Ascensor',
			'terraza: Terraza',
			'patio: Patio',
			'observacion: Observaciones',
			'imagenPrincipal:Imagen Principal',
			'imagen1: Imagen 1',
			'imagen2: Imagen 2',
			'imagen3: Imagen 3',
			'imagen4: Imagen 4',
		}
