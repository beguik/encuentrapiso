from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from .choices import *
from .models import *
from applications.operaciones.models import *
from applications.administracion.models import *
from operator import attrgetter

#Página Principal
class Inicio(View):

    def get(self,request):

        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #cargamos con la función lista_fuc los valores de los choices para poder usuarlos en los select del template
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)
        #limitamos la busqueda de inmuebles a 40 para no sobrecargar los recursos de la página
        #filtramos por activa y ordenamos por fecha de creación
        ofertas=Oferta.objects.all().filter(activa=True).order_by("created_at")[:40]

        #paginación
        paginator=Paginator(ofertas,8)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        
        return render(request,"home.html",{"provincia":provincia,"habitaciones":habitaciones, "ofertas":ofertas,"resultado":resultado,"clientes":clientes,"trabajadores":trabajadores} )

    #filtros del home.
    def post(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)

        #recogemos los datos del POST
        data=request.POST 
        precio=data['precio']
        localidad=data['localidad']
        hab=data['habitaciones']
       
        datos={
        "precio":precio,
        "localidad":localidad,
        "hab":hab,
        }  

        filtro=Inmueble.objects.all().filter(activo=True)
        #recogemos las opciones del filtro que están relacionadas con los inmuebles
        if choices_search(datos["localidad"], PROVINCE_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(localizacion__icontains=choices_search(datos["localidad"], PROVINCE_CHOICES))
        if choices_search(datos["hab"], HABITACIONES_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(habitacion__icontains=choices_search(datos["hab"], HABITACIONES_CHOICES))
        if choices_search(datos["hab"], HABITACIONES_CHOICES) != None and choices_search(datos["localidad"], PROVINCE_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(localizacion__icontains=choices_search(datos["localidad"], PROVINCE_CHOICES)).filter(habitacion__icontains=choices_search(datos["hab"], HABITACIONES_CHOICES))
       
        #hacemos un lista de ofertas con los inmubles seleccionados
        ofertas=[]
        of=Oferta.objects.all().filter(activa=True)

        for o in of:
            for f in filtro:
                if o.inmueble.id == f.id:
                    ofertas.append(o)

        #ordenamos la lista de ofertas si se selecciona una opcion de precio
        if precio == "De Menor a Mayor":
            ofertas.sort(key=attrgetter('precio'))
        if precio == "De Mayor a Menor": 
            ofertas.sort(reverse= True, key=attrgetter('precio'))

        contador=len(ofertas)
        flag=False
        if contador== 0:
            flag= True
            ofertas=Oferta.objects.all().filter(activa=True).order_by("created_at")[:12]

        return render(request,"home.html",{"datos":datos,"flag":flag,"contador":contador,"resultado":ofertas,"provincia":provincia,"habitaciones":habitaciones,"clientes":clientes,"trabajadores":trabajadores,})

#Página de Información de las ofertas
class Informacion(View):
    model=Inmueble
    
    def get(self,request,pk):

        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()

        #Pasamos la lista de favoritos para poder indicar si ya esta agregado en el cliente
        #en el caso de que estuviera entrando en esta página un cliente registrado.
        favoritos=Favoritos.objects.all()

        #la oferta que hemos seleccionado por la id
        inmueble=Oferta.objects.get(id=pk)

        #extraemos un diccionario de ofertas para mostrar en sugerencias
        opciones=Oferta.objects.all().filter(activa=True)
        
        #En la página de información se mostrarán sugerencias 
        #que correspondan con la localidad y tipo de opercion que estamos visitando
        #selecciono una oferta de cada categoría para mostrar al final de la lista de sugerencias
        #para que no quede vacía en el caso de no encontrar coincidencias.
        venta=Oferta.objects.filter(activa=True).filter(tipo=2).order_by("precio")[0]
        alquiler=Oferta.objects.filter(activa=True).filter(tipo=1).order_by("precio")[0]

        return render(request,"informacion.html",{"favoritos":favoritos,"inmueble":inmueble,"opciones":opciones,"clientes":clientes,"trabajadores":trabajadores,"venta":venta,"alquiler":alquiler})

#Esta vista tiene la misma funcionalidad de la página principal pero solo con las Ventas
#se accede a ella desde la pestaña correspondiente en la cabecera. 
class Ventas(View):
    model=Inmueble
    
    def get(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)
        #para poder reutilizar el home nombramos la variable con el mismo nombre "ofertas"
        ofertas=Oferta.objects.all().filter(activa=True).filter(tipo=2).order_by("precio")
       
        paginator=Paginator(ofertas,8)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        titulo="Estas son nuestras mejores ofertas de Venta:"
       
        return render(request,"home.html",{"provincia":provincia,"habitaciones":habitaciones, "ofertas":ofertas,"resultado":resultado,"titulo":titulo,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)

        #recogemos los datos del POST
        data=request.POST 
        precio=data['precio']
        localidad=data['localidad']
        hab=data['habitaciones']
       
        datos={
        "precio":precio,
        "localidad":localidad,
        "hab":hab,
        }

        filtro=Inmueble.objects.all().filter(activo=True)
        #recogemos las opciones del filtro que están relacionadas con los inmuebles
        if choices_search(datos["localidad"], PROVINCE_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(localizacion__icontains=choices_search(datos["localidad"], PROVINCE_CHOICES))
        if choices_search(datos["hab"], HABITACIONES_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(habitacion__icontains=choices_search(datos["hab"], HABITACIONES_CHOICES))
        if choices_search(datos["hab"], HABITACIONES_CHOICES) != None and choices_search(datos["localidad"], PROVINCE_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(localizacion__icontains=choices_search(datos["localidad"], PROVINCE_CHOICES)).filter(habitacion__icontains=choices_search(datos["hab"], HABITACIONES_CHOICES))

        #hacemos un lista de ofertas con los inmubles seleccionados
        ofertas=[]
        of=Oferta.objects.all().filter(activa=True).filter(tipo=2)
        for o in of:
            for f in filtro:
                if o.inmueble.id == f.id:
                    ofertas.append(o)

        #ordenamos la lista de ofertas si se selecciona una opcion de precio
        if precio == "De Menor a Mayor":
            ofertas.sort(key=attrgetter('precio'))
        if precio == "De Mayor a Menor": 
            ofertas.sort(reverse= True, key=attrgetter('precio'))

        contador=len(ofertas)
        flag=False
        if contador== 0:
            flag= True
            ofertas=Oferta.objects.all().filter(activa=True).filter(tipo=2).order_by("created_at")[:12]

        return render(request,"home.html",{"datos":datos,"flag":flag,"contador":contador,"resultado":ofertas,"provincia":provincia,"habitaciones":habitaciones,"clientes":clientes,"trabajadores":trabajadores,})    

#Esta vista tiene la misma funcionalidad de la página principal pero solo con las Ventas
#se accede a ella desde la pestaña correspondiente en la cabecera. 
class Alquileres(View):
    model=Inmueble
    
    def get(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)
        #para poder reutilizar el home nombramos la variable con el mismo nombre "ofertas"
        ofertas=Oferta.objects.all().filter(activa=True).filter(tipo=1).order_by("precio")
        
        paginator=Paginator(ofertas,8)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        titulo="Estas son nuestras mejores ofertas de Alquileres:"
        return render(request,"home.html",{"provincia":provincia,"habitaciones":habitaciones, "ofertas":ofertas,"resultado":resultado,"titulo":titulo,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)

        #recogemos los datos del POST
        data=request.POST 
        precio=data['precio']
        localidad=data['localidad']
        hab=data['habitaciones']
       
        datos={
        "precio":precio,
        "localidad":localidad,
        "hab":hab,
        }

        filtro=Inmueble.objects.all().filter(activo=True)
        #recogemos las opciones del filtro que están relacionadas con los inmuebles
        if choices_search(datos["localidad"], PROVINCE_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(localizacion__icontains=choices_search(datos["localidad"], PROVINCE_CHOICES))
        if choices_search(datos["hab"], HABITACIONES_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(habitacion__icontains=choices_search(datos["hab"], HABITACIONES_CHOICES))
        if choices_search(datos["hab"], HABITACIONES_CHOICES) != None and choices_search(datos["localidad"], PROVINCE_CHOICES) != None:
            filtro=Inmueble.objects.filter(activo=True).filter(localizacion__icontains=choices_search(datos["localidad"], PROVINCE_CHOICES)).filter(habitacion__icontains=choices_search(datos["hab"], HABITACIONES_CHOICES))


        #hacemos un lista de ofertas con los inmubles seleccionados
        ofertas=[]
        of=Oferta.objects.all().filter(activa=True).filter(tipo=1)
        for o in of:
            for f in filtro:
                if o.inmueble.id == f.id:
                    ofertas.append(o)

        #ordenamos la lista de ofertas si se selecciona una opcion de precio
        if precio == "De Menor a Mayor":
            ofertas.sort(key=attrgetter('precio'))
        if precio == "De Mayor a Menor": 
            ofertas.sort(reverse= True, key=attrgetter('precio'))

        contador=len(ofertas)
        flag=False
        if contador== 0:
            flag= True
            ofertas=Oferta.objects.all().filter(activa=True).filter(tipo=1).order_by("created_at")[:12]

        return render(request,"home.html",{"datos":datos,"flag":flag,"contador":contador,"resultado":ofertas,"provincia":provincia,"habitaciones":habitaciones,"clientes":clientes,"trabajadores":trabajadores,})    

#Esta vista nos mostrará el panel principal de un trabajador de la inmobiliaria
class Profesional(View):
    def get(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #se envía un diccionario de ofertas ordenadas por ulima incorporacion
        #en el template se filtrarán para mostrar las que correspondan a la empresa del usuario registrado
        #y a él mismo. 
        ofertas=Oferta.objects.all().order_by('-created_at')[:20]

        return render(request,"profesional.html",{"ofertas":ofertas, "clientes":clientes,"trabajadores":trabajadores} )

#Esta función nos permite trabajar con los campos choices
def choices_search(search="",lista_choise=list()):
    
    if search=="":
        return ""
    for i in lista_choise:
        if i[1]==search:
            return i[0]

#Esta función nos permite organizar las listas.
def lista_fuc(lista=list()):
    lista=list(lista)
    lista_datos=list()
    for i in range(len(lista)):
        lista_datos.append(lista[i][1])
        
    lista_tupla=tuple(lista_datos)
    return lista_tupla

    #función para realizar log informativos

#Esta función nos ha permitido en la parte de pruebas realizar logs informativos
#para depurar el código. 
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()