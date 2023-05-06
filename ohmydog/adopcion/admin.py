from django.contrib import admin
from .models import adopcion

# Register your models here.

class AdopcionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(adopcion, AdopcionAdmin)

