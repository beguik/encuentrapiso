from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.views.generic import View, FormView
from django.contrib import messages
from .forms import *
from .models import *


class SignInView(LoginView):

	template_name = 'login.html'
	

class SignOutView(LogoutView):
    pass

class Registro(View):

	def get(self,request):

		form=CreacionUser()
		formDatos=RegistroForm()
		return render(request,"registroCliente.html",{"form":form, "formDatos":formDatos})

	def post(self,request):
		
		form=CreacionUser(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)
		if form.is_valid():
			if formDatos.is_valid():

				datos=formDatos.cleaned_data
				dni =datos['dni']
				nombre=datos['nombre']
				primer_apellido=datos['primer_apellido']
				segundo_apellido=datos['segundo_apellido']
				telefono=datos['telefono']

				if validarDni(dni):

					if Cliente.objects.filter(dni=dni).exists():
						mensaje="El DNI introducido ya existe"
						return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos, "mensaje":mensaje})

					user=form.save()
					nuevo=Cliente(usuario=user, dni=dni, nombre=nombre, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido, telefono=telefono)
					nuevo.save()
				
					login(request, user)
			
					return redirect('/')
				else: 
					mensajedni="Compruebe que el dni sea correcto"
					return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos, "mensajedni":mensajedni})

		
		else:

			
			for msg in form.error_messages:
				messages.error(request,form.error_messages[msg])
			return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos})


class CuestionarioEmpresa(View):

	def get(self,request):

		form=EncuestaEmpresa()
		return render(request,"cuestionarioEmpresa.html",{"form":form,})

	def post(self,request):
		data=request.POST
		razon_social=data['razon_social'].upper()
		codigo=data['codigo']
		empresas=Empresa.objects.all()
		form=EncuestaEmpresa()
		flag=False
		for e in empresas:
			if e.codigo==codigo:
				flag=True 
		if flag:
			empresa=Empresa.objects.get(codigo=codigo)
			if razon_social == empresa.razon_social.upper():
				em=empresa.id
				return redirect("/registroTrabajador/"+str(em))
			else:
				mensaje="Los datos no son correctos"
				return render(request,"cuestionarioEmpresa.html",{"mensaje":mensaje,"form":form})
		else:
			mensaje="Los datos no son correctos"
			return render(request,"cuestionarioEmpresa.html",{"mensaje":mensaje,"form":form})

class RegistroTrabajador(View):

	def get(self,request,id):
		form=CreacionUser(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)
		empresa=Empresa.objects.get(id=id)
		return render(request,"registroTrabajador.html",{"form":form, "formDatos":formDatos,"empresa":empresa})

	def post(self,request,id):
		form=CreacionUser(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)

		if form.is_valid():
			if formDatos.is_valid():
				empresa=Empresa.objects.get(id=id)
				datos=formDatos.cleaned_data
				dni =datos['dni']
				nombre=datos['nombre']
				primer_apellido=datos['primer_apellido']
				segundo_apellido=datos['segundo_apellido']
				telefono=datos['telefono']

				if validarDni(dni):

					if Trabajador.objects.filter(dni=dni).exists():
						mensajedni="El DNI introducido ya existe"
						return render(request,"registroTrabajador.html",{"form":form,"formDatos":formDatos, "mensajedni":mensajedni})

					user=form.save()
					nuevo=Trabajador(usuario=user, dni=dni, nombre=nombre, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido,empresa=empresa, telefono=telefono)
					nuevo.save()
				
					login(request, user)
			
					return redirect('/profesional/')
				else: 
					mensajedni="Compruebe que el dni sea correcto"
					return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos, "mensajedni":mensajedni})

		
		else:

			
			for msg in form.error_messages:
				messages.error(request,form.error_messages[msg])
			return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos})


#Función para validar dni
def validarDni(dni):

	#tamaño máximo 9 caracteres
	if len(dni)==9:
		#extraemos los numeros
		numeros=int(dni[0:8])
		#extraemos la letra y la ponemos mayúscula
		letra=dni[8:].upper()
		#extraemo el modulo del numero entre 23
		modulo=numeros%23
		#cargamos la clave que nos servirá para validar el resultado
		clave="TRWAGMYFPDXBNJZSQVHLCKET"
		#seleccionamos la key dentro del string clave con el modulo recodio
		key=clave[modulo:modulo+1]
		#verificamos si la letra es la correcta
		if(letra!=key):
			return False
		else:
			return True


#función para realizar log informativos
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()