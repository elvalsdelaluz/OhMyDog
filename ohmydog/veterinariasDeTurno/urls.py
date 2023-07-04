from django.urls import path
from veterinariasDeTurno import views

urlpatterns = [
    path('', views.veterinariasDeTurno, name="veterinariasDeTurno"),
    path('borrar_archivo', views.borrar_archivo, name="borrar_archivo"),
]