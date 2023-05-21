from django.contrib import admin
from .models import donacion, Donante

# Register your models here.

class DonacionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('motivo','finalizacion','created')
    search_field=('motivo')
    list_filter=('finalizacion',)

class DonanteAdmin(admin.ModelAdmin):
    readonly_fields=('fecha',)
    list_display=('dueño','monto','fecha')

admin.site.register(donacion, DonacionAdmin)
admin.site.register(Donante,DonanteAdmin)
# Register your models here.
