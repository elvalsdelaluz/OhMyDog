from django.urls import path
from .views import cerrar_sesion, loguear, vista_registro

urlpatterns=[
    #path('', views.autenticacion, name="autenticacion"),
    path('login', loguear, name="loguear"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
    path('register', vista_registro, name="register"),
]
