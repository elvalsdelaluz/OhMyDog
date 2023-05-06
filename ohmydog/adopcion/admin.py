from django.contrib import admin
from .models import adopcion

# Register your models here.

class AdopcionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('nombre','edad','sexo','tamaño','estado')
    search_field=('nombre')
    list_filter=('edad','sexo','tamaño','estado')

admin.site.register(adopcion, AdopcionAdmin)

