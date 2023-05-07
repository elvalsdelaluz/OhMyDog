from django.db import models

class VeterinariasDeTurno(models.Model):
    imagen = models.ImageField(upload_to='vetTurno')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    