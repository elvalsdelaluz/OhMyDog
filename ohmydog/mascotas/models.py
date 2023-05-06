from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Raza(models.Model):
    raza=models.CharField(max_length=15)

    def __str__(self):
        return self.raza

class mascota(models.Model):
    Sexo=(
        ('0','Hembra'),
        ('1','Macho'),
        ('2','Ns/Nc'),
    )
    nombre=models.CharField(max_length=15, unique=True)
    dueño=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    raza=models.ForeignKey(Raza, on_delete=models.CASCADE)
    nacimiento=models.DateField()
    sexo=models.CharField('Sexo', max_length=1, choices=Sexo)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='mascota'
        verbose_name_plural='mascotas'

    def __str__(self):
        return self.nombre

class libreta_sanitaria(models.Model):
    perro=models.OneToOneField(mascota, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name='libreta'

    def __str__(self):
        return 'Libreta de %{}' %self.perro
    
class entrada_libreta_sanitaria(models.Model):
    Motivo=(
        ('0','Vacuna A'),
        ('1','Vacuna B'),
        ('2','Desparasitario'),
    )
    motivo=models.CharField('Motivo', max_length=1,choices=Motivo)
    peso=models.DecimalField(decimal_places=2, max_digits=5)
    fecha=models.DateTimeField(auto_now_add=True)
    libreta=models.ForeignKey(libreta_sanitaria, on_delete=models.CASCADE)