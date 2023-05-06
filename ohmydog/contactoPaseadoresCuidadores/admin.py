from django.contrib import admin
from .models import proveedor

# Register your models here.

class proveedor_Admin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(proveedor, proveedor_Admin)
# Register your models here.
