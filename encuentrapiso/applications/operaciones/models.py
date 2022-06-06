from django.db import models


class Oferta(models.Model):
	inmueble= models.ForeignKey("inmuebles.Inmueble", verbose_name=("Inmueble"),on_delete=models.CASCADE)
	vendedor=models.ForeignKey("administracion.Trabajador", verbose_name=("trabajador"),on_delete=models.SET_NULL, blank=True,null=True)
	precio=models.DecimalField('Precio', max_digits=13, decimal_places=6)
	descuento=models.DecimalField('Descuento', max_digits=5, decimal_places=2, default=0)
	tipo=models.CharField("tipo",max_length=1)
	activa=models.BooleanField('Activo', default=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return str(self.id)+"-"+str(self.inmueble.id)+" - "+str(self.precio)

	def __gt__(self, oferta):
		return self.precio > oferta.precio

class Venta(models.Model):
	oferta=models.ForeignKey("Oferta",verbose_name=("oferta"),on_delete=models.SET_NULL,null=True )
	comprador=models.ForeignKey("administracion.Cliente", related_name="comprador",verbose_name=("comprador"),on_delete=models.SET_NULL,null=True )
	fecha= models.DateTimeField('Fecha', auto_now=False, auto_now_add=False, null=True,blank=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
		
	def _get_importe(self):
		precio_descuento=self.oferta.precio-((self.oferta.precio*self.oferta.descuento)/100)
		precio_final= precio_descuento+((self.oferta.precio*self.oferta.vendedor.empresa.comision)/100)
		return precio_final
	
	precio_final = property(_get_importe)


	def __str__(self):
		return str(self.oferta.inmueble.id)+" - "+str(self.comprador)+" - "+str(self.precio_final)


class Alquiler(models.Model):
	oferta=models.ForeignKey("Oferta",verbose_name=("oferta"),on_delete=models.SET_NULL,null=True )
	inquilino=models.ForeignKey("administracion.Cliente", related_name="inquilino",verbose_name=("inquilino"), null=True, on_delete=models.SET_NULL, )
	fecha_entrada=models.DateTimeField('Fecha', auto_now=False, auto_now_add=False,blank=True,null=True,)
	meses=models.IntegerField('Meses',)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	

	def _get_precio_final(self):
		#el calculo será el precio por los meses, mas un mes de fianza y uno de comisión
		return (float(self.oferta.precio)*float(self.meses))+(float(self.oferta.precio)*2)

	precio_final = property(_get_precio_final)

	def __str__(self):
		return str(self.oferta.inmueble.id)+" - "+str(self.inquilino)+" - "+str(self.precio_final)
