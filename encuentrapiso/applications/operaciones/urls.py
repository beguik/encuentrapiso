from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_operaciones"

urlpatterns =[ 
	path('simulador/',views.Simulador.as_view(),name="Simulador"),
]


