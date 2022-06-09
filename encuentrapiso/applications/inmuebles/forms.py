from django import forms 
from django.contrib.auth.models import User
from .models import *

class TexArea(forms.Textarea):
	input_type="texarea"

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
				'observacion':TexArea(attrs={'class':'form-control','rows':'10','cols':'5'}),
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