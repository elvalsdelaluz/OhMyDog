from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class donacion(models.Model):#poner en mayus el nombre d la clase
    motivo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=300)
    imagen = models.ImageField(upload_to='donacion', null=True, blank=True)
    finalizacion = models.DateField()
    finalizada = models.BooleanField(default=False)
    id= models.AutoField(primary_key=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Donacion'
        verbose_name_plural='Donaciones'

    def __str__(self):
        return self.motivo
    
class Donante(models.Model):
    campania_donacion = models.ForeignKey(donacion,on_delete=models.CASCADE, default=None)
    dueño=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    monto = models.IntegerField(default=None)
    fecha=models.DateField(auto_now_add=True)


class DonanteNoRegistrado(models.Model):
    campania_donacion = models.ForeignKey(donacion,on_delete=models.CASCADE, default=None)
    nombre=models.CharField(max_length=50)
    monto = models.IntegerField(default=None)
    fecha=models.DateField(auto_now_add=True)


class Tarjeta(models.Model):
    numero = models.CharField(max_length=16)
    nombre_dueño= models.CharField(max_length=50)
    saldo = models.IntegerField(default=None)
    codigo_seguridad = models.CharField(max_length=3)
    mes_vencimiento = models.CharField(max_length=2)
    año_vencimiento = models.CharField(max_length=4)