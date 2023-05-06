from django.db import models

# Create your models here.

class donacion(models.Model):
    motivo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=300)
    finalizacion=models.DateField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
