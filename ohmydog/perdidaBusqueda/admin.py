from django.contrib import admin
from .models import PerroPerdido, Zona

# Register your models here.

class perro_perdido_Admin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('estado','raza','sexo','tamaño','zona')
    list_filter=('estado','zona')

admin.site.register(PerroPerdido, perro_perdido_Admin)
admin.site.register(Zona)

# Register your models here.
