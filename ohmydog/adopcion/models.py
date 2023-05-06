from django.db import models

# Create your models here.

class adopcion(models.Model):
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
        ('0','En adopción'),
        ('1','Adoptado'),
    )
    nombre=models.CharField(max_length=20)
    edad=models.IntegerField()
    comentarios=models.CharField(max_length=100)
    sexo=models.CharField('Sexo',max_length=1, choices=Sexo)
    tamaño=models.CharField('Tamaño',max_length=1, choices=Tamaño)
    estado=models.CharField('Estado', max_length=1, choices=Estado)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='adopcion'
        verbose_name_plural='adopciones'

    def __str__(self):
        return self.nombre
