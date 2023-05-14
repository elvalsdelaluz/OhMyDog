from django.contrib import admin
from .models import Turno

# Register your models here.
class TurnoAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated', 'id')
    list_display=('dueño','mascota','motivo','fecha','estado')
    search_field=('dueño','mascota')
    list_filter=('fecha','estado')

admin.site.register(Turno, TurnoAdmin)