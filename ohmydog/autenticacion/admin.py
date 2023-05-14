from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from autenticacion.models import Cuenta


class CuentaAdmin(UserAdmin):
    list_display = ('email', 'dni', 'numero', 'edad', 'date_joined', 'is_admin', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ['email']

admin.site.register(Cuenta, CuentaAdmin)