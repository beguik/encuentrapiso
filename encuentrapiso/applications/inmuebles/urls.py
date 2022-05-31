from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_inmuebles"

urlpatterns =[ 
	
	path('', views.Inicio.as_view(), name="home"),
	path('info/<pk>',views.Informacion.as_view(),name="Info"),
	path('ventas/',views.Ventas.as_view(),name="Ventas"),
	path('alquileres/',views.Alquileres.as_view(),name="Alquileres"),

]