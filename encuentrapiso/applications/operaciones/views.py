from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from applications.administracion.models import *
from applications.inmuebles.choices import *
from applications.inmuebles.models import *
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from .models import *



class Simulador(View):
    
    def get(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #si no hay post se llama a la plantilla simulador.html solo con los datos de los inmuebles en venta ordendos por precio
        oportunidades= Oferta.objects.all().filter(activa=True).filter(tipo=2).order_by("precio")[:8]
        return render(request,"simulador.html",{"oportunidades":oportunidades,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #si hay post recogemos los datos en un diccionario 
        data=request.POST 
        #extraemos los datos
        capital=data['capital']
        interes=data['intereses']
        plazo=data['plazo'] 
        oportunidades= Oferta.objects.all().filter(activa=True).filter(tipo=2).order_by("precio")[:8]
        flag=True

        #Con esto nos aseguramos que si no se rellenan todos los campos no nos genere un error. 
        if capital == "":
            flag=False
        if interes =="":
            flag=False
        if plazo == "":
            flag=False
        if not flag:
            error="Deben rellenarse todos los campos"
            return render(request, "simulador.html",{"error":error, "oportunidades":oportunidades,"clientes":clientes,"trabajadores":trabajadores})

        # si se han rellenado los campos operamos
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

                
        return render(request, "simulador.html",{"respuesta":respuesta, "cuota":cuota, "oportunidades":oportunidades,"clientes":clientes,"trabajadores":trabajadores})

class Megusta(View):

    def get(self, request, id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #extraemos el usuario
        user=User.objects.get(id=id)
        cliente=Cliente.objects.get(usuario=user)
        #mandamos una lista de favoritos filtrando por el usuario
        favoritos=Favoritos.objects.filter(usuario=cliente)
        #mandamos un contador 
        contador=len(favoritos)
        return render(request,"favoritos.html", {"favoritos":favoritos,"contador":contador,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request, id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #extraemos los datos del post en data
        data=request.POST
        fav=data['fav']
        #buscamos el favorito con la id enviada
        favorito=Favoritos.objects.get(id=fav)
        #borramos
        favorito.delete()
        #redireccionamos a la misma página
        return redirect('/favoritos/'+str(id))

def AddFavorito(request):
    
    #recogemos los datos del post
    data=request.POST
    usu=data['usuario']
    of=data['oferta'] 
    #buscamos el usuario 
    user=User.objects.get(id=usu)
    usuario=Cliente.objects.get(usuario=user)
    oferta=Oferta.objects.get(id=data['oferta'])
    #creamos registro de favorito con el usuario y la oferta
    Favoritos.objects.create( oferta=oferta,usuario=usuario)
    #devolvemos en la misa dirección
    return redirect('/info/'+str(of))
    
class Comprar(View):

    def get(self, request,pk):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        # buscamos la oferta con la id enviada
        oferta=Oferta.objects.get(id=pk)
        #mandamos un listado de ventas para en la vista controlar si esa petición ya se ha generado
        ventas=Venta.objects.all()
        
        return render(request,"comprar.html",{"oferta":oferta,"ventas":ventas,"clientes":clientes,"trabajadores":trabajadores})

def exportarPdf(request):
    #extraemos datos
    data=request.POST
    usu=data['usuario']
    of=data['oferta']

    oferta=Oferta.objects.get(id=of)
    usuario=User.objects.get(id=usu)
    cliente=Cliente.objects.get(usuario=usuario)
    vent=Venta.objects.all()

    #Comprobamos que la solicidud no está generada y si ya estuviera generada enviamos a las operaciones
    for v in vent:
        if v.oferta == oferta and v.comprador == cliente:
            return redirect('/')


    #generamos venta    
    venta=Venta.objects.create(oferta=oferta, comprador=cliente)

    #creamos contexto
    contexto={'venta':venta,}

    #renderizamos nuestro archivo_pdf.html y el contexto
    html=render_to_string('archivo_pdf.html',contexto)

    #informamos al navegador que le vamos a pasar un pdf para que el navegador de el tratamiento oportuno
    response=HttpResponse(content_type="application/pdf")
    response["Content-Disposition"]="inline; archivo.pdf"

    #establece las reglas de manejo de los estilos
    font_config=FontConfiguration()

    #el atributo base_url establece la ruta absoluta para poder cargar imagenes.
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)
    
    return response

class Operaciones(View):

    def get(self, request, id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #extraemos el usuario
        user=User.objects.get(id=id)
        cliente=Cliente.objects.get(usuario=user)
        ventas=Venta.objects.filter(comprador=cliente)
        alquileres=Alquiler.objects.filter(inquilino=cliente)
        #mandamos un contador 
        contVentas=len(ventas)
        contAlquileres=len(alquileres)

        #genero el contexto fuera 
        contexto={
        "clientes":clientes,
        "trabajadores":trabajadores,
        "ventas":ventas,
        "contVentas":contVentas,
        "alquileres":alquileres,
        "contAlquileres":contAlquileres
        }

        return render(request,"operaciones.html",contexto)
    def post(self, request, id):
        


#función para realizar log informativos
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()