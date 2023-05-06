from django.db import models
from mascotas.models import Raza
# Create your models here.

class Zona(models.Model):
    zona=models.CharField(max_length=25)

    def __str__(self):
        return self.zona

class Estado(models.Model):
    estado=models.CharField(max_length=10)

    def __str__(self):
        return self.estado

class perro_perdido(models.Model):
    Sexo=(
        ('0','Hembra'),
        ('1','Macho'),
        ('2','Ns/Nc'),
    )
    Tamaño=(
        ('0','Chico: entre 3 y 10 kilos'),
        ('1', 'Mediano: entre 10 y 25 kilos'),
        ('2', 'Grande: entre 25 y 50 kilos'),
        ('3','Gigante: más de 50 kilos'),
    )
    Estado=(
        ('0','Buscando dueño'),
        ('1','Buscando perro'),
        ('2','Reunidos'),
    )
    estado=models.CharField('Estado', max_length=1, choices=Estado)
    tamaño=models.CharField('Tamaño', max_length=1, choices=Tamaño)
    raza=models.ForeignKey(Raza, on_delete=models.CASCADE)
    sexo=models.CharField('Sexo', max_length=1, choices=Sexo)
    zona=models.ForeignKey(Zona, on_delete=models.CASCADE)
    comentario=models.CharField(max_length=50, null=True, blank=True)
    foto=models.ImageField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
