from django.db import models
from applications.operaciones.models import *
from django.contrib.auth.models import User


class Inmueble(models.Model):

	PROVINCE_CHOICES =(
		('01', 'Alaba'), ('02', 'Albacete'), ('03', 'Alicante'), 
		('04', 'Almería'), ('05', 'Ávila'), ('06', 'Badajoz'), 
		('07', 'Islas Baleares'), ('08', 'Barcelona'), ('09', 'Burgos'), 
		('10', 'Cáceres'), ('11', 'Cádiz'), ('12', 'Castellón'), 
		('13', 'Ciudad Real'), ('14', 'Córdoba'), ('15', 'A Coruña'), 
		('16', 'Cuenca'), ('17', 'Girona'), ('18', 'Granada'), 
		('19', 'Guadalajara'), ('20', 'Guipúzcoa'), ('21', 'Huelva'), 
		('22', 'Huesca'), ('23', 'Jaén'), ('24', 'León'), 
		('25', 'Lleida'), ('26', 'La Rioja'), ('27', 'Lugo'), 
		('28', 'Madrid'), ('29', 'Málaga'), ('30', 'Murcia'), 
		('31', 'Navarra'), ('32', 'Ourense'), ('33', 'Asturias'), 
		('34', 'Palencia'), ('35', 'Las Palmas'), ('36', 'Pontevedra'), 
		('37', 'Salamanca'), ('38', 'Santa Cruz de Tenerife'), ('39', 'Cantabria'), 
		('40', 'Segovia'), ('41', 'Sevilla'), ('42', 'Soria'), 
		('43', 'Tarragona'), ('44', 'Teruel'), ('45', 'Toledo'), 
		('46', 'Valencia'), ('47', 'Valladolid'), ('48', 'Vizcaya'), 
		('49', 'Zamora'), ('50', 'Zaragoza'), ('51', 'Ceuta'), ('52', 'Melilla')
		)

	HABITACIONES_CHOICES=(
        ('0', 'Loft'),
        ('1', '1 Habitacion'),
        ('2', '2 Habitaciones'),
        ('3', '3 Habitaciones'),
        ('4', '4 Habitaciones'),
        ('5', '5 Habitaciones'),
        ('6', 'Más de 5'),
        )

	ORIENTACION_CHOICES=(
	 	('1', '(N) Norte'),
        ('2', '(NO) Noreste'),
        ('3', '(E) Este'),
        ('4', '(SE) Sureste'),
        ('5', '(S) Sur'),
        ('6', '(SO) Suroeste'),
        ('7', '(O) Oeste'),
        ('8', '(NO) Noroeste'),

	 	)

	propietario= models.ForeignKey("administracion.Propietario", verbose_name="propietario",on_delete=models.CASCADE )
	direccion= models.CharField('Direccion', max_length=200)
	localizacion= models.CharField('Localización', max_length=2, choices=PROVINCE_CHOICES)
	codigo_postal= models.IntegerField('CP',)
	metros=models.IntegerField('Metros',)
	habitacion=models.CharField('Habitación', max_length=1, choices=HABITACIONES_CHOICES)
	planta=models.IntegerField('Planta',)
	wc=models.IntegerField('Baños',)
	orientacion=models.CharField('Orientación', max_length=1, choices=ORIENTACION_CHOICES)
	construccion=models.IntegerField('Año Construcción',)
	comunidad=models.DecimalField('Precio Comunidad', max_digits=6, decimal_places=2)
	ascensor=models.BooleanField('Ascensor', default=False)
	terraza=models.BooleanField('Terraza', default=False)
	patio=models.BooleanField('Patio', default=False)
	observacion= models.CharField('Observacion', max_length=1024)
	imagenPrincipal= models.ImageField("ImagenPrincipal",upload_to="imagenes/")
	imagen1=models.ImageField("imagen1",upload_to="imagenes/",default="imagenes/pordefecto.png",blank=True, null=True)
	imagen2=models.ImageField("imagen2",upload_to="imagenes/",default="imagenes/pordefecto.png",blank=True, null=True)
	imagen3=models.ImageField("imagen3",upload_to="imagenes/",default="imagenes/pordefecto.png",blank=True, null=True)
	imagen4=models.ImageField("imagen4",upload_to="imagenes/",default="imagenes/pordefecto.png",blank=True, null=True)
	activo=models.BooleanField('Activo', default=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		referencia=str(self.id)+"-"+str(self.direccion)
		return referencia

class Favoritos(models.Model):
	oferta=models.ForeignKey("operaciones.Oferta",on_delete=models.CASCADE)
	usuario=models.ForeignKey("administracion.Cliente",on_delete=models.CASCADE)

	def __str__(self):
		referencia=str(self.oferta)+"-"+str(self.usuario)
		return referencia
