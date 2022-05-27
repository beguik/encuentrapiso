from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from applications.inmuebles.choices import *
from .models import *
from applications.inmuebles.models import *




class Simulador(View):

    def get(self, request):
    	
    	return render(request,"simulador.html")

    def post(self, request):

    	data=request.POST

    	capital=data['capital']
    	interes=data['intereses']

    	plazo=data['plazo']
    	interesMensual=(float(interes)/12)
    	numeroMeses=(float(plazo)*12)
    

    	respuesta={
    	"capital":capital,
    	"interes":interes,
    	"plazo":plazo
    	}



    	cuota=float(capital)*((((1+(interesMensual/100))**numeroMeses)*(interesMensual/100))/(((1+(interesMensual/100))**numeroMeses)-1))        
    	
    	return render(request, "simulador.html",{"respuesta":respuesta, "cuota":cuota})

