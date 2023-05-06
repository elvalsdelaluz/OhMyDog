from django.contrib import admin
from .models import perro_perdido, Zona

# Register your models here.

class perro_perdido_Admin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('estado','raza','sexo','tamaño','zona')
    list_filter=('estado','zona')

admin.site.register(perro_perdido, perro_perdido_Admin)
admin.site.register(Zona)

# Register your models here.
