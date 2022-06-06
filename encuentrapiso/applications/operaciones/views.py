from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from datetime import datetime, timedelta 
from dateutil.relativedelta import relativedelta
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
            return redirect('/operaciones/'+usu)


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
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #extraemos los datos del post en data
        
        data=request.POST
        iduser=data["user"]

        if "venta" in request.POST:
            idventa=data["venta"]
            venta=Venta.objects.get(id=idventa)
            venta.delete()

        if "alquiler" in request.POST:
            idalquiler=data["alquiler"]
            alquiler=Alquiler.objects.get(id=idalquiler)
            alquiler.delete()
        
        return redirect('/operaciones/'+str(id))

class Alquilar(View):
    def get(self, request,pk):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        # buscamos la oferta con la id enviada
        oferta=Oferta.objects.get(id=pk)
        #extraemos los alquileres
        alquileres=Alquiler.objects.all()
        lista=list()

        #creamos una lista con los alquileres del inmueble solicidtado
        for a in alquileres:
            if a.oferta.inmueble == oferta.inmueble:
                lista.append(a)

        #contamos si hay mas de un alquiler de ese inmueble
        contador=len(lista)
        logs("contador",contador)
        #si la lista no contiene resultados retornamos la página sin valores extras
        if contador == 0:
            calendario=datetime.now().strftime('%Y-%m-%d')
            calendarioFin=datetime.today() + timedelta(days=20)
            calFin=str(calendarioFin)[0:10]
            logs("calendario",calendario)
            logs("calendarioFin",calendarioFin)
            return render(request,"alquilar.html",{"calendario":calendario,"calFin":calFin, "oferta":oferta,"clientes":clientes,"trabajadores":trabajadores})
        
        #si hay mas de 0 buscamos la fecha más alta 
        else:
            fecha=lista[0].fecha_entrada
            meses=lista[0].meses
            for l in lista:
                if fecha<l.fecha_entrada:
                    fecha=l.fecha_entrada
                    meses=l.meses

            fechaInicio=str(fecha)
            fechaformato=fechaInicio[0:10]
            fechaInicial = datetime.strptime(fechaformato, '%Y-%m-%d')
            fechaFin=fechaInicial+relativedelta(months=meses)
            #como en el template no se permite operar extraemos la fecha más los 20 días establecidos 
            #para poder seleccionar la fecha de entrada del próximo alquiler
            fechaFinPlantilla=fechaFin+relativedelta(days=20)
            fechaFinFormato=str(fechaFin)[0:10]
            fechaFinReserva=str(fechaFinPlantilla)[0:10]

            return render(request,"alquilar.html",{"fechaFinReserva":fechaFinReserva,"fechaFinFormato":fechaFinFormato,"fechaFin":fechaFin, "alquileres":alquileres,"oferta":oferta,"clientes":clientes,"trabajadores":trabajadores})


def alquilarPdf(request):
    data=request.POST
    usu=data['usuario']
    of=data['oferta']
    fecha=data['fecha']
    meses=data['meses']
    logs("dta",data)

    fecha_inicio = datetime.strptime(fecha, '%Y-%m-%d')

    oferta=Oferta.objects.get(id=of)
    usuario=User.objects.get(id=usu)
    cliente=Cliente.objects.get(usuario=usuario)
    alq=Alquiler.objects.all()
    
    #controlamos que no pueda duplicarse el alquiler, si el inquilino ya tiene un alquiler que coincida con las fechas
    #se le reenviara a su pagina de operaciones
    lista=list()
    for a in alq:
        if a.oferta == oferta and a.inquilino == cliente:
            lista.append(a)

    if len(lista)>0:
        l=lista[-1]
        m=l.meses
        fechaAnterior=l.fecha_entrada
        fechaAnt=str(a.fecha_entrada)
        fechFor=fechaAnt[0:10]
        fechaAntFor=datetime.strptime(fechFor, '%Y-%m-%d')
        fechaSalida=fechaAntFor+relativedelta(months=m)

        fechNueva=datetime.strptime(fecha, '%Y-%m-%d')
        
        if fechaSalida > fechNueva:
            logs("fechaSalida",fechaSalida)
            logs("fechaNueva",fechNueva)
            return redirect('/operaciones/'+usu)



    alquiler=Alquiler.objects.create(oferta=oferta, inquilino=cliente, fecha_entrada=fecha_inicio, meses=meses)

    #creamos contexto
    contexto={'alquiler':alquiler,}

    #renderizamos nuestro archivo_pdf.html y el contexto
    html=render_to_string('alquiler_pdf.html',contexto)

    #informamos al navegador que le vamos a pasar un pdf para que el navegador de el tratamiento oportuno
    response=HttpResponse(content_type="application/pdf")
    response["Content-Disposition"]="inline; archivo.pdf"

    #establece las reglas de manejo de los estilos
    font_config=FontConfiguration()

    #el atributo base_url establece la ruta absoluta para poder cargar imagenes.
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)
    
    return response

        











#función para realizar log informativos
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()