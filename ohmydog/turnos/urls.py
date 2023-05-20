from django.urls import path
from turnos import views


urlpatterns = [
    path('', views.publicacion, name="mis_turnos"),
    path('turnos_pendientes/', views.ver_turnos_pendientes, name="turnos_pendientes"),
    path('turnos_activos/', views.ver_turnos_activos, name="turnos_activos"),
    path('turnos_pasados/', views.ver_turnos_pasados, name="turnos_pasados"),
    path('turnos_pendientes/aceptar/<int:pk>', views.aceptar_turno, name="aceptar_turno"),
    path('turnos_pendientes/rechazar/<int:pk>', views.rechazar_turno, name="rechazar_turno"),
    path('motivo_rechazo/<str:motivo>', views.ver_motivo_rechazo, name="motivo_rechazo"),
    path('<int:pk>', views.cancelar_turno, name="cancelar_turno"),
    path('turnos_activos/concluir/<int:pk>', views.concluir_turno, name="concluir_turno"),
    path('historia_turno/<int:pk>', views.ver_historia_turno, name="historia_turno"),


]