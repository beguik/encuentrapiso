from django.contrib import admin
from .models import *
from applications.administracion.models import *
from applications.inmuebles.models import *

class OfertaAdmin(admin.ModelAdmin):
	list_display=(
		'id',
		'inmueble',
		'vendedor',
		'precio',
		'tipo',
		'activa',
		)
	search_fields=(
		'inmueble',
		'vendedor',
		)
	list_filter=(
		'inmueble',
		'vendedor',
		)
admin.site.register(Oferta,OfertaAdmin)

class VentaAdmin(admin.ModelAdmin):
	list_display=(
		'oferta',
		'comprador',
		'precio_final',
		'fecha',
		)
	search_fields=(
		'oferta',
		'comprador',
		'fecha',

		)
	list_filter=(
		'oferta',
		'comprador',
		'fecha'
		)
admin.site.register(Venta,VentaAdmin)

class AlquilerAdmin(admin.ModelAdmin):
	list_display=(
		'oferta',
		'inquilino',
		'fecha_entrada',
		'meses',
		'precio_final',
		)
	search_fields=(
		'oferta'
		'inquilino',
		'fecha_entrada',
		'precio_final',

		)
	list_filter=(
		'oferta',
		'inquilino',
		'fecha_entrada',
		)
admin.site.register(Alquiler,AlquilerAdmin)