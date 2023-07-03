from django.db import models
from perdidaBusqueda.models import Zona

# Create your models here.


class Proveedor(models.Model):

    Roles= (
        ('0','Paseador'),
        ('1','Cuidador')
    )
    nombre=models.CharField(max_length=15)
    apellido=models.CharField(max_length=15)
    email=models.EmailField()
    telefono=models.CharField(max_length=10)
    zona=models.ForeignKey(Zona, on_delete=models.CASCADE)
    rol=models.CharField('Trabajo', max_length=1, choices=Roles)
    direccion=models.CharField(max_length=20, default='', blank=True)
    baja=models.BooleanField(null=True, blank=True)
    fecha_baja=models.DateField(default=None, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='proveedor'
        verbose_name_plural='proveedores'

    def __str__(self):
        return self.nombre
    
