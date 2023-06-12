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
    list_query=enumerate(list_query)
    #Tengo que convertir los int en str porque sino el formulario se queja
    list_query_casteada=[]
    for num, raza in list_query:
        casteada=(str(num), raza)
        list_query_casteada.append(casteada)
    return list_query_casteada

class Mascota(models.Model): #va con mayus. Mascota. xD
    sexo_choices=[
        ('0','Hembra'),
        ('1','Macho'),
        ('2','Ns/Nc'),
    ]
    razas_choices = convertir_queryset(Raza.objects.all())

    nombre=models.CharField(max_length=50)
    dueño=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True) #tuve que sacar el User xq es el modelo predeterminado de python. Nosotros usamos el custom.

    raza=models.CharField('Raza', max_length=1, choices=razas_choices)
    fecha_nacimiento=models.DateField()
    sexo=models.CharField('Sexo', max_length=1, choices=sexo_choices)
    observaciones=models.TextField(blank=True, null=True)
    #foto=models.ImageField()
    id = models.AutoField(primary_key=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='mascota'
        verbose_name_plural='mascotas'

    def __str__(self):
        return self.nombre

    
class EntradaLibretaSanitaria(models.Model):
    Motivo=(
        ('0','Vacuna A'),
        ('1','Vacuna B'),
        ('2','Desparasitario'),
    )
    motivo=models.CharField('Motivo', max_length=1,choices=Motivo)
    peso=models.DecimalField(decimal_places=2, max_digits=5)
    fecha=models.DateField(editable=True)
    perro=models.ForeignKey(Mascota, on_delete=models.CASCADE, default=None)
    #cantidad_desparasitario=.models.DecimalField()