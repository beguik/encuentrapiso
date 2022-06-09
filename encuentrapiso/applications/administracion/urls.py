from django.urls import path
from django.contrib import admin
from . import views 

app_name = "app_administracion"

urlpatterns =[ 
	
	path('login/', views.SignInView.as_view(), name='login'),
	path('logout/', views.SignOutView.as_view(), name='logout'),
	path('registro/', views.Registro.as_view(), name="registroCliente"),
	path('cuestionarioEmpresa/', views.CuestionarioEmpresa.as_view(), name="cuestionarioEmpresa"),
	path('registroTrabajador/<int:id>', views.RegistroTrabajador.as_view(), name="RegistroTrabajador"),
]