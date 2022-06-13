from django.urls import path
from django.contrib import admin

from . import views 

app_name = "app_operaciones"

urlpatterns =[ 
	path('simulador/',views.Simulador.as_view(),name="Simulador"),
	path('favoritos/<int:id>/',views.Megusta.as_view(),name="Favoritos"),
	path('addfavoritos/',views.AddFavorito, name="addFavorito"),
	path('comprar/<pk>',views.Comprar.as_view(), name="comprar"),
	path('pdf/', views.comprarPdf, name="Pdf"),
	path('operaciones/<int:id>/',views.Operaciones.as_view(),name="Operaciones"),
	path('desactivarVenta/<int:id>/', views.desactivarVenta.as_view(),name="desactivarVenta"),
	path('desactivarAlquiler/<int:id>/', views.desactivarAlquiler.as_view(),name="desactivarAlquiler"),
	path('alquilar/<pk>', views.Alquilar.as_view(),name="Alquilar"),
	path('alquilarPdf/', views.alquilarPdf, name="AlquilarPdf"),
	path('crearOferta/', views.CrearOferta.as_view(), name="CrearOferta"),
	path('gestion/<int:id>', views.Gestion.as_view(), name="Gestion"),
	path('eliminarV/<int:id>/', views.EliminarV.as_view(),name="EliminarV"),
	path('eliminarA/<int:id>/', views.EliminarA.as_view(),name="EliminarA"),
	
]


