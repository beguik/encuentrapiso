from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_inmuebles"

urlpatterns =[ 
	
	path('', views.Inicio.as_view(), name="home"),
	path('info/<pk>',views.Informacion.as_view(),name="Info"),
	path('ofertas/',views.Ofertas.as_view(),name="Ofertas"),

]