from django.contrib import admin
from .models import donacion, Donante, DonanteNoRegistrado, Tarjeta

# Register your models here.

class DonacionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('motivo','finalizacion','created')
    search_field=('motivo')
    list_filter=('finalizacion',)

class DonanteAdmin(admin.ModelAdmin):
    readonly_fields=('fecha',)
    list_display=('dueño','monto','fecha')
class DonanteNoRegistradoAdmin(admin.ModelAdmin):
    readonly_fields=('fecha',)
    list_display=('nombre','monto','fecha')

class TarjetaAdmin(admin.ModelAdmin):
    list_display=('numero','nombre_dueño','saldo','año_vencimiento','mes_vencimiento','codigo_seguridad')


admin.site.register(donacion, DonacionAdmin)
admin.site.register(Donante,DonanteAdmin)
admin.site.register(Tarjeta,TarjetaAdmin)
admin.site.register(DonanteNoRegistrado,DonanteNoRegistradoAdmin)
# Register your models here.
