from django.contrib import admin
from .models import Mascota, EntradaLibretaSanitaria, Raza

# Register your models here.

class MascotaAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('nombre','dueño','raza','sexo')
    search_field=('nombre','dueño')

class EntradaLibretaSanitariaAdmin(admin.ModelAdmin):
    readonly_field=('fecha')
    list_display=('motivo','peso','fecha')
    list_filter=('fecha',)
    
admin.site.register(Mascota, MascotaAdmin)
admin.site.register(EntradaLibretaSanitaria,EntradaLibretaSanitariaAdmin)
admin.site.register(Raza)

