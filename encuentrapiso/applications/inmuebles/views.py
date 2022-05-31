from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from .choices import *
from .models import *
from applications.operaciones.models import *
from applications.administracion.models import *

class Inicio(View):

    def get(self,request):

        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #cargamos con la función lista_fuc los valores de los choices para poder usuarlos en los select del template
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)
        #limitamos la busqueda de inmuebles a 20 para no sobrecargar los recursos de la página
        #filtramos por activa y ordenamos por fecha de creación
        ofertas=Oferta.objects.all().filter(activa=True).order_by("created_at")[:20]

        #paginación
        paginator=Paginator(ofertas,8)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)

        return render(request,"home.html",{"provincia":provincia,"habitaciones":habitaciones, "ofertas":ofertas,"resultado":resultado,"clientes":clientes,"trabajadores":trabajadores})
 

class Informacion(View):
    model=Inmueble
    
    def get(self,request,pk):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #paso una oferta de venta y de alquiler para poder mostrar por defecto en la página de información
        venta=Oferta.objects.filter(activa=True).filter(tipo=2).order_by("precio")[0]
        alquiler=Oferta.objects.filter(activa=True).filter(tipo=1).order_by("precio")[0]


        inmueble=Oferta.objects.get(id=pk)
        opciones=Oferta.objects.all().filter(activa=True)
        return render(request,"informacion.html",{"inmueble":inmueble,"opciones":opciones,"clientes":clientes,"trabajadores":trabajadores,"venta":venta,"alquiler":alquiler})


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





def lista_fuc(lista=list()):
    lista=list(lista)
    lista_datos=list()
    for i in range(len(lista)):
        lista_datos.append(lista[i][1])
        
    lista_tupla=tuple(lista_datos)
    return lista_tupla