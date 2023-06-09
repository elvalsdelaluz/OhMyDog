from django.contrib import admin
from .models import Adopcion

# Register your models here.

class AdopcionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated', 'id')
    list_display=('nombre','fecha_nacimiento','sexo','tamaño','estado')
    search_field=('nombre')
    list_filter=('fecha_nacimiento','sexo','tamaño','estado')

admin.site.register(Adopcion, AdopcionAdmin)

