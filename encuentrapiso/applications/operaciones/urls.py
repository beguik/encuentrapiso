from django.urls import path
from django.contrib import admin

from . import views 

app_name = "app_operaciones"

urlpatterns =[ 
	path('simulador/',views.Simulador.as_view(),name="Simulador"),
	path('favoritos/<int:id>/',views.Megusta.as_view(),name="Favoritos"),
	path('addfavoritos/',views.AddFavorito, name="addFavorito"),
	path('comprar/<pk>',views.Comprar.as_view(), name="comprar"),
	path('pdf/', views.exportarPdf, name="Pdf"),
	path('operaciones/<int:id>/',views.Operaciones.as_view(),name="Operaciones"),
	path('alquilar/<pk>', views.Alquilar.as_view(),name="Alquilar"),
	path('alquilarPdf/', views.alquilarPdf, name="AlquilarPdf")


]


