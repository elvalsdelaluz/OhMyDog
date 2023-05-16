from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class Raza(models.Model):
    raza=models.CharField(max_length=15)

    def __str__(self):
        return self.raza

def convertir_queryset(query):
    list_query =[]
    for obj in query:
        list_query.append(obj.raza)
    return list(enumerate(list_query))

class Mascota(models.Model): #va con mayus. Mascota. xD
    Sexo=(
        ('0','Hembra'),
        ('1','Macho'),
        ('2','Ns/Nc'),
    )

    nombre=models.CharField(max_length=50)
    dueño=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True) #tuve que sacar el User xq es el modelo predeterminado de python. Nosotros usamos el custom.

    raza=models.ForeignKey(Raza, on_delete=models.CASCADE, choices=convertir_queryset(Raza.objects.all()))
    fecha_nacimiento=models.DateField()
    sexo=models.CharField('Sexo', max_length=1, choices=Sexo)
    observaciones=models.TextField(blank=True, null=True)
    #foto=models.ImageField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='mascota'
        verbose_name_plural='mascotas'

    def __str__(self):
        return self.nombre

class LibretaSanitaria(models.Model):
    perro=models.OneToOneField(Mascota, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name='libreta'

    def __str__(self):
        return 'Libreta de %{}' %self.perro
    
class EntradaLibretaSanitaria(models.Model):
    Motivo=(
        ('0','Vacuna A'),
        ('1','Vacuna B'),
        ('2','Desparasitario'),
    )
    motivo=models.CharField('Motivo', max_length=1,choices=Motivo)
    peso=models.DecimalField(decimal_places=2, max_digits=5)
    fecha=models.DateTimeField(auto_now_add=True)
    libreta=models.ForeignKey(LibretaSanitaria, on_delete=models.CASCADE)