from django.urls import path
from .views import alta_mascota, ver_mis_mascotas, ver_historial_turnos, ver_libreta_sanitaria, editar_mi_mascota

urlpatterns=[
    path('alta_mascota', alta_mascota, name="alta_mascota"),
    path('ver_mis_mascotas', ver_mis_mascotas, name="ver_mis_mascotas"),
    path('ver_historial_turnos/<int:mascota_id>/', ver_historial_turnos, name="ver_historial_turnos"),
    path('ver_libreta_sanitaria/<int:mascota_id>/', ver_libreta_sanitaria, name="ver_libreta_sanitaria"),
    path('editar_mi_mascota/<int:mascota_id>/', editar_mi_mascota, name="editar_mi_mascota")
]
