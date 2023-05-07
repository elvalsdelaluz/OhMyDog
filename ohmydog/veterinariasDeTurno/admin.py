from django.contrib import admin
from .models import VeterinariasDeTurno
class VeterinariasDeTurnoAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(VeterinariasDeTurno, VeterinariasDeTurnoAdmin)