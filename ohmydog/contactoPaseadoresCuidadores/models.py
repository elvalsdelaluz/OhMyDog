from django.db import models
from perdidaBusqueda.models import Zona

# Create your models here.


class proveedor(models.Model):

    Roles= (
        ('0','Paseador'),
        ('1','Cuidador')
    )
    nombre=models.CharField(max_length=30)
    email=models.EmailField()
    telefono=models.CharField(max_length=10)
    zona=models.ForeignKey(Zona, on_delete=models.CASCADE)
    rol=models.CharField('Trabajo', max_length=1, choices=Roles)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)