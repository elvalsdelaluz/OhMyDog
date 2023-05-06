from django.contrib import admin
from .models import donacion

# Register your models here.

class DonacionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(donacion, DonacionAdmin)
# Register your models here.
