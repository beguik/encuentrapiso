from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from datetime import datetime, timedelta 
from dateutil.relativedelta import relativedelta
from applications.administracion.models import *
from applications.administracion.forms import *
from applications.inmuebles.choices import *
from applications.inmuebles.models import *
from applications.inmuebles.forms import *
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from .models import *
from .forms import *

#Esta clase nos lleva a la pestaña de simulación del pago de una hipoteca 
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

#Esta clase nos manda a la pestaña de favoritos accesible solo desde el cliente
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
        #borramos -- al no tratarse de una operación especialmente relevante y que puede deshacerse facilmente no generamos pantalla de confirmación. 
        favorito.delete()
        #redireccionamos a la misma página
        return redirect('/favoritos/'+str(id))

#función que nos permite añadir a favoritos, está función será accesible solo desde el cliente
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
   
#Esta clase genera una solicitud de Compra.
#Creará una Venta con el campo activo a True y el aprobado a False.
#Esta clase será solo accesible desde el cliene
#pero afectara al panel de administración del Trabajador.  
class Comprar(View):

    def get(self, request,pk):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        # buscamos la oferta con la id enviada
        oferta=Oferta.objects.get(id=pk)
        #mandamos un listado de ventas para en la vista controlar si esa petición ya se ha generado
        ventas=Venta.objects.all()
        
        return render(request,"comprar.html",{"oferta":oferta,"ventas":ventas,"clientes":clientes,"trabajadores":trabajadores})

#Esta función genara un pdf con todos los datos de la Venta. 
def comprarPdf(request):
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

#Esta clase genera una solicitud de Alquiler.
#Creará un Alquiler con el campo activo a True y el aprobado a False y baja a False, tal como se define en el modelo. 
#Esta clase será solo accesible desde el cliene
#pero afectara al panel de administración del Trabajador.  
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

        #si la lista no contiene resultados retornamos la página sin valores extras
        if contador == 0:
            calendario=datetime.now().strftime('%Y-%m-%d')
            calendarioFin=datetime.today() + timedelta(days=20)
            calFin=str(calendarioFin)[0:10]
            return render(request,"alquilar.html",{"calendario":calendario,"calFin":calFin, "oferta":oferta,"clientes":clientes,"trabajadores":trabajadores})
        
        #si hay mas de 0 buscamos la fecha más alta 
        else:
            fechaFin=lista[0].fecha_fin
            for l in lista:
                if fechaFin<l.fecha_fin:
                    fechaFin=l.fecha_fin

            
            fechafinFormato=str(fechaFin)[0:10]
            fechaFormtao=datetime.strptime(fechafinFormato, '%Y-%m-%d')
            fechaFinPlantilla=fechaFin+relativedelta(days=20)
            fechaFPlantilla=str(fechaFinPlantilla)[0:10]
            logs("fecha",fechaFPlantilla)

            return render(request,"alquilar.html",{"fechaFin":fechaFin,"fechafinFormato":fechafinFormato, "fechaFPlantilla":fechaFPlantilla, "alquileres":alquileres,"oferta":oferta,"clientes":clientes,"trabajadores":trabajadores})

#Esta función genara un pdf con todos los datos del Alquiler.
def alquilarPdf(request):
    data=request.POST
    usu=data['usuario']
    of=data['oferta']
    fecha=data['fecha']
    meses=data['meses']
   
    fecha_inicio = datetime.strptime(fecha, '%Y-%m-%d')

    oferta=Oferta.objects.get(id=of)
    usuario=User.objects.get(id=usu)
    cliente=Cliente.objects.get(usuario=usuario)
    alq=Alquiler.objects.all()
    
    #controlamos que no pueda duplicarse el alquiler, si el inquilino ya tiene un alquiler que coincida con las fechas
    #se le reenviara a su pagina de operaciones
    
    flag=False
    for a in alq:
        if a.oferta == oferta and a.inquilino == cliente:
            fechaC = str(fecha)[0:10]
            fechaFC=str(a.fecha_fin)[0:10]
            if fechaC <= fechaFC:
                flag=True

    if flag:
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
        
#Esta clase presenta un listado de todas las operaciones del cliente
#En el template se filtrará por solicitudes pendientes o aprobadas.       
class Operaciones(View):

    def get(self, request, id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        #extraemos el usuario
        user=User.objects.get(id=id)
        cliente=Cliente.objects.get(usuario=user)
        ventas=Venta.objects.filter(comprador=cliente).filter(activa=True).filter(aprobada=False)
        alquileres=Alquiler.objects.filter(inquilino=cliente).filter(activa=True).filter(aprobada=False)
        ventasConfirmadas=Venta.objects.filter(comprador=cliente).filter(aprobada=True).filter(activa=True)
        alquileresConfirmados=Alquiler.objects.filter(inquilino=cliente).filter(aprobada=True).filter(activa=True)
        #mandamos un contador 
        contVSolicitadas=len(ventas)
        contASolicitados=len(alquileres)
        contAaprobadas=len(alquileresConfirmados)
        contVaprobadas=len(ventasConfirmadas)

        #genero el contexto fuera 
        contexto={
        "clientes":clientes,
        "trabajadores":trabajadores,
        "ventas":ventas,
        "contVSolicitadas":contVSolicitadas,
        "alquileres":alquileres,
        "contASolicitados":contASolicitados,
        "ventasConfirmadas":ventasConfirmadas,
        "alquileresConfirmados":alquileresConfirmados,
        "contAaprobadas":contAaprobadas,
        "contVaprobadas":contVaprobadas
        }

        return render(request,"operaciones.html",contexto)

#El cliente no podrá nunca eliminar una solicitud de Venta o de Alquiler
#En el caso de que ya no este interesado podrá desctivar la solicitud lo que quedará reflejado en el panel del Trabjador
#Solo el trabajdor podrá eliminar la solicitud. 
class desactivarVenta(View):

    def get(self, request, id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        venta=Venta.objects.get(id=id)

        return render(request, "eliminar.html",{"venta":venta,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request, id):
        data=request.POST
        iduser=data["user"]
        idventa=data["venta"]
        venta=Venta.objects.get(id=idventa)
        #modifico el atributo activo y guardo el objeto Venta. 
        venta.activa=False
        venta.save()
        
        return redirect('/operaciones/'+str(iduser))

class desactivarAlquiler(View):

    def get(self, request, id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        alquiler=Alquiler.objects.get(id=id)

        return render(request, "eliminar.html",{"alquiler":alquiler,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request, id):
        data=request.POST
        iduser=data["user"]
        idalquiler=data["alquiler"]
        alquiler=Alquiler.objects.get(id=idalquiler)

        #filtro en este caso por si el alquiler ya está aprobado 
        #modifico los atributos y guardo.  
        if alquiler.aprobada==True:
            alquiler.baja=True
            alquiler.activa=False
            alquiler.save()
        else:
            alquiler.activa=False
            alquiler.save()
        
        return redirect('/operaciones/'+str(iduser))

#Esta clase contempla mucha información puesto que para crear una oferta primero debe existir el inmueble y para crear un inmueble debe existir el propietario
class CrearOferta(View):

    def get(self,request):
       
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()

        #se mandan los formularios de creacion de oferta, inmueble y propietario al template
        formularioInmueble= addInmueble()
        formularioPropietario=PropietarioForm()
        formularioOferta=addOferta()
        fecha=datetime.now().strftime('%Y-%m-%d')
        year=str(fecha)[:4]

        return render (request, "crearOferta.html",{"formularioOferta":formularioOferta,"formularioPropietario":formularioPropietario,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})

    def post(self,request):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        formularioInmueble= addInmueble()
        formularioPropietario=PropietarioForm()
        formularioOferta=addOferta()
        fecha=datetime.now().strftime('%Y-%m-%d')
        year=str(fecha)[:4]
        validaciones=[]
        

        data=request.POST
        #recogemos los datos del post y filtramos, si hay propietario se crea
        if 'propietario' in data:
            #Si hay propietario se va a crear un inmueble. 
            
            #aunque en el cliente se han validado todos los campos se vuelven a comprobar aquí 
            #para que cuando se inserten en la base de datos no haya problemas
            erroresInmueble=[]
            
            propietario=data['propietario']
            if propietario=="":
                validaciones.append(False)
                erroresInmueble.append("Debe seleccionar un propietario")
            else:
                pro=Propietario.objects.get(id=propietario)

            direccion=data['direccion']
            if direccion=="":
                validaciones.append(False)
                erroresInmueble.append("Debe indicar una direccion")

            localizacion=data['localizacion']
            if not localizacion.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar una localización")

            cp=data['codigo_postal']
            if not cp.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar un codigo postal")
           
            construccion=data['construccion']
            if not construccion.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar el año de construccion")

            metros=data['metros']
            if not metros.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar los metros")
                
            habitacion=data['habitacion']
            if not habitacion.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar el número de habitaciones")

            planta=data['planta']
            if not planta.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar el número de planta")
           
            wc=data['wc']
            if not wc.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar el número de baños")

            orientacion=data['orientacion']
            if not orientacion.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe indicar la orientación")

            comunidad=data['comunidad']
            if not planta.isdigit():
                validaciones.append(False)
                erroresInmueble.append("Debe el precio de la comunidad")

            if 'ascensor' in data:
                ascensor=True
            else:
                ascensor=False 

            if 'terraza' in data:
                terraza=True
            else:
                terraza=False 

            if 'patio' in data:
                patio=True
            else:
                patio=False 

            observacion=data['observacion']
            if observacion=="":
                validaciones.append(False)
                erroresInmueble.append("Debe rellenar el campo observaciones con los elementos más destacados del inmueble")

            #el request.Files me permite cargar las imagenes.
            if "imagenPrincipal" in request.FILES:
                handle_uploaded_file(request.FILES['imagenPrincipal'])
                imagenPrincipal=f"imagenes/{request.FILES['imagenPrincipal'].name}"
            else:
                validaciones.append(False)
                erroresInmueble.append("La imagen principal del inmueble es requerida")
            
            #los campos anteriores son obligarios por lo que una vez terminada con imagen principal 
            #se comprueba si ha habido errores y si los hay se devuelve a la pantalla con la informacion
            if False in validaciones:
                error="Revise los errores ocurridos en la pestaña correspondiente."
                return render(request, "crearOferta.html",{"formularioOferta":formularioOferta,"formularioPropietario":formularioPropietario,"error":error,"erroresInmueble":erroresInmueble,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})

            #si las siguientes estan en el request se recogen sino se pone la imagen por defecto. 
            if "imagen1" in request.FILES:
                handle_uploaded_file(request.FILES['imagen1'])
                imagen1=f"imagenes/{request.FILES['imagen1'].name}"
            else:
                imagen1="imagenes/pordefecto.png"

            if "imagen2" in request.FILES:
                handle_uploaded_file(request.FILES['imagen2'])
                imagen2=f"imagenes/{request.FILES['imagen2'].name}"
            else:
                imagen2="imagenes/pordefecto.png"

            if "imagen3" in request.FILES:
                handle_uploaded_file(request.FILES['imagen3'])
                imagen3=f"imagenes/{request.FILES['imagen3'].name}"
            else:
                imagen3="imagenes/pordefecto.png"

            if "imagen4" in request.FILES:
                handle_uploaded_file(request.FILES['imagen4'])
                imagen4=f"imagenes/{request.FILES['imagen4'].name}"
            else:
                imagen4="imagenes/pordefecto.png"

            #con todos los datos se crea el inmueble. 
            Inmueble.objects.create(propietario=pro, direccion=direccion, localizacion=localizacion,
            codigo_postal=cp, metros=metros, habitacion=habitacion, planta=planta, wc=wc,
            orientacion=orientacion, construccion=construccion, comunidad=comunidad, ascensor=ascensor,
            terraza=terraza, patio=patio, observacion=observacion, imagenPrincipal=imagenPrincipal, imagen1=imagen1,
            imagen2=imagen2, imagen3=imagen3, imagen4=imagen4 )
            
            mensajeRegistro= "Inmueble Creado Correctamente"
            #se envia a la misma pantalla y se informa de que se ha creado correctamente.
            return render(request, "crearOferta.html",{"formularioOferta":formularioOferta,"formularioPropietario":formularioPropietario,"mensajeRegistro":mensajeRegistro,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})

        if 'dni' in data:
            erroresPropietario=[] 
            dni=data['dni']
            #si hay dni se va a crear un propietario
            #igualmente se validan los campos y si todo es correcto se crea, sino se nos devuelve a la pantalla con el error corespondiente. 

            if validarDni(dni):
                if Propietario.objects.filter(dni=dni).exists():
                    mensajedni="El DNI introducido ya existe"
                    error="Revise los errores ocurridos en la pestaña correspondiente."
                    return render (request, "crearOferta.html",{"formularioOferta":formularioOferta,"error":error,"mensajedni":mensajedni, "formularioPropietario":formularioPropietario,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})
                else:
                    nombre=data['nombre']
                    if nombre=="":
                        validaciones.append(False)
                        erroresPropietario.append("Debe indicar un nombre")

                    primerApellido=data['primer_apellido']
                    if primerApellido=="":
                        validaciones.append(False)
                        erroresPropietario.append("Debe indicar un primer apellido")

                    segundoApellido=data['segundo_apellido']
                    if segundoApellido=="":
                        validaciones.append(False)
                        erroresPropietario.append("Debe indicar un segundo apellido")

                    telefono=data['telefono']
                    if nombre=="":
                        validaciones.append(False)
                        erroresPropietario.append("Debe indicar un telefono")

                    if False in validaciones:
                        error="Revise los errores ocurridos en la pestaña correspondiente."
                        return render(request, "crearOferta.html",{"formularioOferta":formularioOferta,"error":error,"formularioPropietario":formularioPropietario,"error":error,"erroresPropietario":erroresPropietario,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})
                    else:
                        Propietario.objects.create(dni=dni, nombre=nombre, primer_apellido=primerApellido, segundo_apellido=segundoApellido, telefono=telefono)
                        mensajeRegistro= "Propietario Creado Correctamente"
                        return render(request, "crearOferta.html",{"formularioOferta":formularioOferta,"formularioPropietario":formularioPropietario,"mensajeRegistro":mensajeRegistro,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})

            else:
                mensajedni="El DNI introducido no es correcto"
                return render (request, "crearOferta.html",{"formularioOferta":formularioOferta,"mensajedni":mensajedni, "formularioPropietario":formularioPropietario,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})

        if 'inmueble' in data:
            
            erroresOferta=[]
            #si hay un inmueble se va a crear una oferta y se realizan las mismas validaciones anteriores.

            usuario=data['usuario']
            user=User.objects.get(id=usuario)
            trabajador=Trabajador.objects.get(usuario=user)
            
            inmueble=data['inmueble']
            if inmueble=="":
                validaciones.append(False)
                erroresOferta.append("Debe seleccionar un inmueble")
            else:
                inmueb=Inmueble.objects.get(id=inmueble)
                #comprobamos que el inmueble no este desactivado
                if not inmueb.activo:
                    validaciones.append(False)
                    erroresOferta.append("El inmueble no se encuentra activo actualmente.")

            precio=data['precio']  
            try:
                float(precio)
            except ValueError:
                validaciones.append(False)
                erroresOferta.append("Debe introducir un precio real")
          
            descuento=data['descuento']
            try:
                float(descuento)
            except ValueError:
                validaciones.append(False)
                erroresOferta.append("Debe introducir un descuento real")
            if float(descuento)>100:
                validaciones.append(False)
                erroresOferta.append("Debe introducir un descuento real")

            tipo=data['tipo']
            if int(tipo)==1 or int(tipo)==2:
                logs("tipo",tipo)
            else:
                validaciones.append(False)
                erroresOferta.append("Debe introducir un tipo real")
            
            if False in validaciones:
                error="Revise los errores ocurridos en la pestaña correspondiente."
                return render(request, "crearOferta.html",{"formularioOferta":formularioOferta,"formularioPropietario":formularioPropietario,"error":error,"erroresOferta":erroresOferta,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})     
           
            Oferta.objects.create(inmueble=inmueb, vendedor=trabajador,precio=precio,descuento=descuento)
            mensajeRegistro="Oferta creada correctamente. "
            return render(request, "crearOferta.html",{"formularioOferta":formularioOferta,"formularioPropietario":formularioPropietario,"mensajeRegistro":mensajeRegistro,"year":year,"formularioInmueble":formularioInmueble,"clientes":clientes,"trabajadores":trabajadores})

#Con esta vista el Trabajador podrá ver las nuevas solicitudes, aprobarlas, eliminarlas y revisarlas. 
class Gestion(View):

    def get(self, request,id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        user=User.objects.get(id=id)
        trabajador=Trabajador.objects.get(usuario=user)
        #creamos dos listas con las ventas y alquileres correspondientes al trabajador registrado
        ventasT=[]
        alquilerT=[]

        ventas=Venta.objects.all()
        for v in ventas:
            if v.oferta.vendedor == trabajador:
                ventasT.append(v)

        alquileres=Alquiler.objects.all()
        for a in alquileres:
            if a.oferta.vendedor == trabajador:
                alquilerT.append(a)
        
        return render(request, "gestion.html",{"alquilerT":alquilerT,"ventasT":ventasT,"clientes":clientes,"trabajadores":trabajadores})

    def post(self,request,id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        user=User.objects.get(id=id)
        trabajador=Trabajador.objects.get(usuario=user)
        ventasT=[]
        alquilerT=[]

        data=request.POST
        
        #recibe los datos del formulario para aprobar
        if 'aprobar' in data:

            if 'venta' in data:
                venta=data['venta']
                vent=Venta.objects.get(id=venta)
                #desactivamos el inmueble
                idinmueble=vent.oferta.inmueble.id
                inmueble=Inmueble.objects.get(id=idinmueble)
                inmueble.activo=False 
                inmueble.save()
                #aprobamos la venta
                vent.aprobada=True
                vent.save()

            if 'alquiler' in data:
                alquiler=data['alquiler']
                alq=Alquiler.objects.get(id=alquiler)
                alq.aprobada=True
                alq.save()

        #recibe los datos del formulario para desaprobar
        if 'desaprobar' in data:

            if 'venta' in data:
                venta=data['venta']
                vent=Venta.objects.get(id=venta)
                #activamos el inmueble
                idinmueble=vent.oferta.inmueble.id
                inmueble=Inmueble.objects.get(id=idinmueble)
                inmueble.activo=True 
                inmueble.save()
                #desaprobamos la venta.
                vent.aprobada=False
                vent.save()

            if 'alquiler' in data:
                alquiler=data['alquiler']
                alq=Alquiler.objects.get(id=alquiler)
                alq.aprobada=False
                alq.save()

        #recibe los datos del formulario para volver a activar 
        #todas las solicitudes se activan por defecto al crearse pero un cliente puede desactivarla
        #el trabajador por tanto tendrá la opcion de volver a activarla. 
        if 'activar' in data:

            if 'venta' in data:
                venta=data['venta']
                vent=Venta.objects.get(id=venta)
                vent.activa=True
                vent.save()

            if 'alquiler' in data:
                
                alquiler=data['alquiler']
                alq=Alquiler.objects.get(id=alquiler)
                alq.activa=True
                alq.baja=False
                alq.save()

        ventas=Venta.objects.all()
        for v in ventas:
            if v.oferta.vendedor == trabajador:
                ventasT.append(v)

        alquileres=Alquiler.objects.all()
        for a in alquileres:
            if a.oferta.vendedor == trabajador:
                alquilerT.append(a)


        return render(request, "gestion.html",{"alquilerT":alquilerT,"ventasT":ventasT,"clientes":clientes,"trabajadores":trabajadores})

#Las dos clases siguientes: EliminarV y EliminarA
#presenta una pantalla de confirmación para que la eliminación de una solicitud no se realice por error. 
class EliminarV(View):
    def get(self,request,id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        venta=Venta.objects.get(id=id)

        return render(request, "gestionEliminarV.html",{"venta":venta,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request, id):
        data=request.POST
        iduser=data["user"]

        if 'venta' in data:
            venta=data['venta']
            vent=Venta.objects.get(id=venta)
            vent.delete()
        return redirect('/gestion/'+str(iduser))

class EliminarA(View):
    def get(self,request,id):
        clientes=Cliente.objects.all()
        trabajadores=Trabajador.objects.all()
        alquiler=Alquiler.objects.get(id=id)

        return render(request, "gestionEliminarA.html",{"alquiler":alquiler,"clientes":clientes,"trabajadores":trabajadores})

    def post(self, request, id):
        data=request.POST
        iduser=data["user"]

        if 'alquiler' in data:
            alquiler=data['alquiler']
            alq=Alquiler.objects.get(id=alquiler)
            alq.delete()
        
        return redirect('/gestion/'+str(iduser))

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

#función para cargar las imagenes
def handle_uploaded_file(f):
    with open(f'media/imagenes/{f.name}', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#Esta función nos ha permitido en la parte de pruebas realizar logs informativos
#para depurar el código. 
def logs(file="log",mensaje=""):
    escribir = open(file+".txt", "a")
    escribir.write(str(mensaje)+"\n")
    escribir.close()