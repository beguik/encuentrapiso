from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.views.generic import View, FormView
from django.contrib import messages
from .forms import *
from .models import *

#Esta vista nos redirige al login.html y Django se encarga de gestionar el lógin
#nosotros debemos configurar los parametros correctos en el archivo settings. 
class SignInView(LoginView):

	template_name = 'login.html'
	
#Igualmente Django se encarga del logout, pero debemos nombrar la función y configurarlas 
#en las rutas. 
class SignOutView(LogoutView):
    pass

#Clase para registrar clientes. 
class Registro(View):

	def get(self,request):
		#instaciamos los formularios creados en el archivo forms.py 
		#el formulario CreacionUser se encargará del modelo User
		#el formulario RegistroForm se ecargará del resto de datos del modelo Cliente
		form=CreacionUser()
		formDatos=RegistroForm()
		return render(request,"registroCliente.html",{"form":form, "formDatos":formDatos})

	def post(self,request):
		
		form=CreacionUser(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)
		
		if form.is_valid():
			
			if formDatos.is_valid():
				#extraemos los datos
				datos=formDatos.cleaned_data
				dni =datos['dni']
				nombre=datos['nombre']
				primer_apellido=datos['primer_apellido']
				segundo_apellido=datos['segundo_apellido']
				telefono=datos['telefono']
				
				#validamos el DNI (aunque previamente se ha validado en cliente)
				if validarDni(dni):
					
					#comprobamos que el cliente no exite, y si existe devolvermos a la misma pantalla con un mensaje informando de que ese dni ya existe. 
					if Cliente.objects.filter(dni=dni).exists():
						mensaje="El DNI introducido ya existe"
						return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos, "mensaje":mensaje})
					
					#si todo es correcto salvamos primero el user
					user=form.save()
					
					#y despues creamos el nuevo cliente con el usuario=user y todos los campos recogidos en el data
					nuevo=Cliente(usuario=user, dni=dni, nombre=nombre, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido, telefono=telefono)
					nuevo.save()
					
					#hacemos login
					login(request, user)
					
					#redirigimos al inicio
					return redirect('/')
				
				else: 
					#si el dni no es correcto devolvemos a la pantalla informado
					mensajedni="Compruebe que el dni sea correcto"
					return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos, "mensajedni":mensajedni})
		
		else:
			#si el formulario no es valido recogemos los mensajes y los enviamos al template para mostrarlos. 
			for msg in form.error_messages:
				messages.error(request,form.error_messages[msg])
			
			return render(request,"registroCliente.html",{"form":form,"formDatos":formDatos})

#Para que un usuario se registre como trabajador debe de pertenecer a una empresa
#y deberá facilitar los datos de la empresa para tener acceso al registro como trabajador. 
class CuestionarioEmpresa(View):

	def get(self,request):

		form=EncuestaEmpresa()
		return render(request,"cuestionarioEmpresa.html",{"form":form,})

	def post(self,request):
		
		#recogemos los datos del post
		data=request.POST
		razon_social=data['razon_social'].upper()
		codigo=data['codigo']
		
		#extraemos un listado de empresas
		empresas=Empresa.objects.all()
		
		form=EncuestaEmpresa()

		#comprobamos que los datos introducidos correspondan a una de las empresas registradas
		#si la comprobación no es correcta retornamos al formulario indicando que los datos no son correctos
		#si la comprobación es correcta permitimos el registro como cliente y enviamos la empresa a la plantilla de registro
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

#Registro de un trabajador que recibe por parametro la id de la empresa a la que irá asociado. 
class RegistroTrabajador(View):

	def get(self,request,id):
		#se instancias los cuestionarios
		form=CreacionUser(request.POST)
		formDatos=RegistroForm(request.POST,request.FILES)
		#se extrae la empresa de la id recibida por parametro
		empresa=Empresa.objects.get(id=id)
		#se envía al template de registro con los datos extraidos anterioremnte. 
		return render(request,"registroTrabajador.html",{"form":form, "formDatos":formDatos,"empresa":empresa})

	def post(self,request,id):
		#al igual que en el cliente, estraemos los datos del post, validamos y si todo es correcto 
		#creamos al Trabajador y le enviamos a su panel profesional. 
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
			#si se han cometido errores en el formulario se recogen y se envian al template. 
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


#Esta función nos ha permitido en la parte de pruebas realizar logs informativos
#para depurar el código. 
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()