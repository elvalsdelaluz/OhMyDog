from django.db import models
from mascotas.models import Raza, Mascota
from django.contrib.auth import get_user_model
from datetime import date
# Create your models here.

class Zona(models.Model): #creo que no es necesario, preguntar, define el al atributo de tipo charField
    zona=models.CharField(max_length=25)

    def __str__(self):
        return self.zona

class Estado(models.Model):
    estado=models.CharField(max_length=10)

    def __str__(self):
        return self.estado
    
def user_directory_path(perdido, filename):
    #file will be uploaded to MEDIA_ROOT/user <id>/<filename>
    return 'perrosPerdidos/user_{0}/{1}'.format(perdido.dueño.id, filename)
    

class PerroPerdido(models.Model):
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
        ('0','Extraviado'),
        ('1','Encontrado'),
        ('2','Localizado'),
    )
    dueño=models.ForeignKey(get_user_model(),on_delete=models.CASCADE, null=True) #info del dueño de la publicacion
    nombre = models.CharField('Nombre', max_length=30, blank=True, null=True)
    foto=models.ImageField(upload_to=user_directory_path, blank=True, null=True, max_length=256)
    fecha_perdido=models.DateField(default=date.today, editable=True) #hay que chequear que no se pierda mañana
    fecha_nacimiento=models.DateField(default=None, null=True) #para sacar la edad 
    estado=models.CharField('Estado', max_length=1, choices=Estado)
    tamaño=models.CharField('Tamaño', max_length=1, choices=Tamaño)
    #raza=models.ForeignKey(Raza, on_delete=models.CASCADE)
    raza=models.CharField('Raza', max_length=2, choices=Mascota.razas_choices)
    sexo=models.CharField('Sexo', max_length=1, choices=Sexo)
    #zona=models.ForeignKey(Zona, on_delete=models.CASCADE) #creo que no es necesario, preguntar
    zona=models.CharField(max_length=50, null=True, blank=True)
    comentario=models.CharField(max_length=50, null=True, blank=True)

    id = models.AutoField(primary_key=True)
   
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
