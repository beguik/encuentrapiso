from django.contrib import admin
from .models import *

#Configuración del panel de Administración de Django para los modelos:
#Empresa, Propietario, Cliente y Trabajador.

class EmpresaAdmin(admin.ModelAdmin):
	list_display=(
		'cif',
		'nombre_empresa',
		'razon_social',
		'comision',
		'codigo'
		)
	search_fields=(
		'cif',
		'nombre_empresa',
		'codigo'
		)
	list_filter=(
		'cif',
		'nombre_empresa',
		'razon_social',
		)

admin.site.register(Empresa,EmpresaAdmin)

class PropietarioAdmin(admin.ModelAdmin):
	list_display=(
		'dni',
		'nombre',
		'primer_apellido',
		'segundo_apellido',
		'telefono',
		)
	search_fields=(
		'nombre',
		'telefono',
		'dni',

		)
	list_filter=(
		'nombre',
		'telefono',
		'dni',
		)

admin.site.register(Propietario,PropietarioAdmin)

class ClienteAdmin(admin.ModelAdmin):
	list_display=(
		'usuario',
		'dni',
		'nombre',
		'primer_apellido',
		'segundo_apellido',
		'telefono'
		)
	search_fields=(
		'nombre',
		'telefono',
		'dni'

		)
	list_filter=(
		'nombre',
		'telefono',
		'dni'
		)

admin.site.register(Cliente,ClienteAdmin)

class TrabajadorAdmin(admin.ModelAdmin):
	list_display=(
		'usuario',
		'dni',
		'nombre',
		'primer_apellido',
		'segundo_apellido',
		'empresa',
		'telefono'
		)
	search_fields=(
		'nombre',
		'telefono',
		'dni',
		'empresa'

		)
	list_filter=(
		'nombre',
		'telefono',
		'dni'
		)

admin.site.register(Trabajador,TrabajadorAdmin)
