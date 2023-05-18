from django.urls import path
from turnos import views


urlpatterns = [
    path('', views.publicacion, name="mis_turnos"),
    path('turnos_pendientes/', views.ver_turnos_pendientes, name="turnos_pendientes"),
    path('turnos_activos/', views.ver_turnos_activos, name="turnos_activos"),
    path('turnos_pasados/', views.ver_turnos_pasados, name="turnos_pasados"),
    path('turnos_pendientes/<int:pk>', views.aceptar_turno, name="aceptar_turno"),

]