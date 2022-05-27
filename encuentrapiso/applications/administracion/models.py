from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Empresa(models.Model):
    cif=models.CharField('CIF', max_length=9, unique=True)
    nombre_empresa=models.CharField('Nombre', max_length=100)
    razon_social=models.CharField('Razon Social', max_length=100)
    comision=models.DecimalField('Comisión', max_digits=4, decimal_places=2, default=3)
    codigo=models.CharField('Codigo',max_length=10)
    def __str__(self):
        return self.nombre_empresa

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField('DNI', max_length=9, unique=True)
    nombre = models.CharField('Nombre', max_length=25)
    primer_apellido = models.CharField('1ºApellido', max_length=50)
    segundo_apellido = models.CharField('2ºApellido', max_length=50)
    telefono= PhoneNumberField(blank=True)

    def __str__(self): 
        return self.primer_apellido+" "+self.segundo_apellido+", "+self.nombre

class Trabajador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField('DNI', max_length=9, unique=True)
    nombre = models.CharField('Nombre', max_length=25)
    primer_apellido = models.CharField('1ºApellido', max_length=50)
    segundo_apellido = models.CharField('2ºApellido', max_length=50)
    empresa = models.ForeignKey("Empresa", verbose_name=("Empresa"), on_delete=models.CASCADE, blank=True, null=True)
    telefono= PhoneNumberField(blank=True)

    def __str__(self): 
        return self.primer_apellido+" "+self.segundo_apellido+", "+self.nombre


class Propietario(models.Model):
    dni = models.CharField('DNI', max_length=9, unique=True)
    nombre = models.CharField('Nombre', max_length=25)
    primer_apellido = models.CharField('1ºApellido', max_length=50)
    segundo_apellido = models.CharField('2ºApellido', max_length=50)
    telefono= PhoneNumberField(blank=True)


    def __str__(self): 
        return self.primer_apellido+" "+self.segundo_apellido+", "+self.nombre