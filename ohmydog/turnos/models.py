from django.db import models
from django.contrib.auth import get_user_model
from mascotas.models import Mascota


User=get_user_model()
# Create your models here.
class Turno(models.Model):
    motivos = (
        ('0','Consulta General'),
        ('1', 'Vacuna A'),
        ('2', 'Vacuna B'),
        ('3', 'Desparasitacion'),
        ('4', 'Urgencia Intermedia'),
        ('5','Castracion'),
    )
    franja = (
        ('0','Mañana'),
        ('1','Tarde'),
    )
    estados=(
        ('0','Pendiente'),
        ('1','Aceptado'),
        ('2','Rechazado'),
        ('3','Cancelado'),
        ('4','Cerrado'),
    )

    dueño=models.ForeignKey(User, on_delete=models.CASCADE)
    mascota=models.ForeignKey(Mascota, on_delete=models.CASCADE)#no deberia ser una mascota de las q tiene registrada?
    motivo=models.CharField('Motivo',max_length=1,choices=motivos)
    franjaHoraria=models.CharField('Franja horaria',max_length=1,choices=franja)
    fecha=models.DateField()
    estado=models.CharField('Estado',max_length=1,choices=estados)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name='turno'
        verbose_name_plural='turnos'


