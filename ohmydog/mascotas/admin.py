from django.contrib import admin
from .models import mascota, entrada_libreta_sanitaria, libreta_sanitaria, Raza

# Register your models here.

class mascota_Admin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('nombre','dueño','raza','sexo')
    search_field=('nombre','dueño')

class entrada_libreta_admin(admin.ModelAdmin):
    readonly_field=('fecha')
    list_display=('motivo','peso','fecha')
    list_filter=('fecha',)
    
admin.site.register(mascota, mascota_Admin)
admin.site.register(entrada_libreta_sanitaria,entrada_libreta_admin)
admin.site.register(libreta_sanitaria)
admin.site.register(Raza)

