from django.contrib import admin
from .models import *
from applications.administracion.models import*
from django.utils.html import format_html


class InmuebleAdmin(admin.ModelAdmin):
	list_display=(
		'img',
		'id',
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
		'created_at',
		'activo',
		)

	search_fields=(
		'propietario',
		'codigo_postal',
		'construccion',
		'activo',

		)
	list_filter=(
		'propietario',
		'codigo_postal',
		'construccion',
		'activo',
		)

	def img(self,obj):
		return format_html('<img src={} width="35" height="35"/>',obj.imagenPrincipal.url)

admin.site.register(Inmueble,InmuebleAdmin)

class FavoritosAdmin(admin.ModelAdmin):
	list_display=(
		'inmueble',
		'usuario',
		)
	search_fields=(
		'usuario',

		)
	list_filter=(
		'usuario',
		)

admin.site.register(Favoritos,FavoritosAdmin)