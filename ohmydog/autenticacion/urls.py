from django.urls import path
from .views import cerrar_sesion, loguear

urlpatterns=[
    #path('', views.autenticacion, name="autenticacion"),
    path('loguear', loguear, name="loguear"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
]
