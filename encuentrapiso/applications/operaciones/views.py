from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from applications.inmuebles.choices import *
from .models import *
from applications.inmuebles.models import *




class Simulador(View):

    def get(self, request):
        #si no hay post se llama a la plantilla simulador.html solo con los datos de los inmuebles en venta ordendos por precio
        oportunidades= Oferta.objects.all().filter(activa=True).filter(tipo=2).order_by("precio")[:8]
        return render(request,"simulador.html",{"oportunidades":oportunidades})

    def post(self, request):
        
        #si hay post recogemos los datos en un diccionario 
        data=request.POST 
        #extraemos los datos
        capital=data['capital']
        interes=data['intereses']
        plazo=data['plazo']
        #operamos
        interesMensual=(float(interes)/12)
        numeroMeses=(float(plazo)*12)
        cuota=float(capital)*((((1+(interesMensual/100))**numeroMeses)*(interesMensual/100))/(((1+(interesMensual/100))**numeroMeses)-1))        
        
        #generamos una respueta
        respuesta={
        "capital":capital,
        "interes":interes,
        "plazo":plazo
        }

        #creamos un diccionario con sugerencias
        oportunidades= Oferta.objects.all().filter(activa=True).filter(tipo=2).order_by("precio")[:8]

                
        return render(request, "simulador.html",{"respuesta":respuesta, "cuota":cuota, "oportunidades":oportunidades})










#función para realizar log informativos
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()