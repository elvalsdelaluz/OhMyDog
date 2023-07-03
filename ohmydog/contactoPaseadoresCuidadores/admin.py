from django.contrib import admin
from .models import Proveedor

# Register your models here.

class proveedor_Admin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('nombre','apellido','email','telefono','zona','rol')
    search_field=('apellido')
    list_filter=('zona','rol')

admin.site.register(Proveedor, proveedor_Admin)
# Register your models here.
