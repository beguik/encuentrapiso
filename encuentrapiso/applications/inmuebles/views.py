from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from .choices import *
from .models import *
from applications.operaciones.models import *

class Inicio(View):
   

    def get(self,request):
        #cargamos con la función lista_fuc los valores de los choices para poder usuarlos en los select del template
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)
        #limitamos la busqueda de inmuebles a 50 para no sobrecargar los recursos de la página
        ofertas=ofertaVenta.objects.all().filter(activa=True).order_by("inmueble_id")
        paginator=Paginator(ofertas,8)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)

        return render(request,"home.html",{"provincia":provincia,"habitaciones":habitaciones, "ofertas":ofertas,"resultado":resultado})
 



class Informacion(View):
    model=Inmueble
    def get(self,request,pk):
        inmueble=ofertaVenta.objects.get(id=pk)
        return render(request,"informacion.html",{"inmueble":inmueble,})


class Ofertas(View):
    model=Inmueble
    def get(self, request):
        provincia= lista_fuc(PROVINCE_CHOICES)
        habitaciones= lista_fuc(HABITACIONES_CHOICES)
        ofertas=ofertaVenta.objects.all().filter(activa=True).order_by("precio")
        paginator=Paginator(ofertas,8)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)
        titulo="Estas son nuestras mejores ofertas:"
        return render(request,"home.html",{"provincia":provincia,"habitaciones":habitaciones, "ofertas":ofertas,"resultado":resultado,"titulo":titulo})





def lista_fuc(lista=list()):
    lista=list(lista)
    lista_datos=list()
    for i in range(len(lista)):
        lista_datos.append(lista[i][1])
        
    lista_tupla=tuple(lista_datos)
    return lista_tupla