# Generated by Django 4.0.3 on 2022-05-31 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inmuebles', '0001_initial'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=6, max_digits=13, verbose_name='Precio')),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Descuento')),
                ('tipo', models.CharField(max_length=1, verbose_name='tipo')),
                ('activa', models.BooleanField(default=True, verbose_name='Activo')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('inmueble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmuebles.inmueble', verbose_name='Inmueble')),
                ('vendedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administracion.trabajador', verbose_name='trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True, verbose_name='Fecha')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('comprador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comprador', to='administracion.cliente', verbose_name='comprador')),
                ('oferta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='operaciones.oferta', verbose_name='oferta')),
            ],
        ),
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateTimeField(blank=True, null=True, verbose_name='Fecha')),
                ('meses', models.IntegerField(verbose_name='Meses')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('inquilino', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inquilino', to='administracion.cliente', verbose_name='inquilino')),
                ('oferta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='operaciones.oferta', verbose_name='oferta')),
            ],
        ),
    ]
