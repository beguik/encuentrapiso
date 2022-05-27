from django.contrib import admin
from .models import *
from applications.administracion.models import *
from applications.inmuebles.models import *

class OfertaVentaAdmin(admin.ModelAdmin):
	list_display=(
		'inmueble',
		'vendedor',
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
admin.site.register(ofertaVenta,OfertaVentaAdmin)

class VentaAdmin(admin.ModelAdmin):
	list_display=(
		'oferta',
		'comprador',
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

class OfertaAlquilerAdmin(admin.ModelAdmin):
	list_display=(
		'inmueble',
		'vendedor',
		'precio_mes',
		'descuento',
		'comision',
		'activa'
		)
	search_fields=(
		'inmueble',
		'vendedor',
		'precio_mes',
		
		)
	list_filter=(
		'inmueble',
		'vendedor',
		'precio_mes',
		)
admin.site.register(ofertaAlquiler,OfertaAlquilerAdmin)


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