from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class donacion(models.Model):#poner en mayus el nombre d la clase
    motivo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=300)
    imagen = models.ImageField(upload_to='donacion', null=True, blank=True)
    finalizacion = models.DateField()
    finalizada = models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Donacion'
        verbose_name_plural='Donaciones'

    def __str__(self):
        return self.motivo
    
class Donante(models.Model):
    dueño=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    monto = models.IntegerField(default=None)
    fecha=models.DateField(auto_now_add=True)


class DonanteNoRegistrado(models.Model):
    nombre=models.CharField(max_length=50)
    monto = models.IntegerField(default=None)
    fecha=models.DateField(auto_now_add=True)


