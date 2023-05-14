from django.urls import path
from turnos import views


urlpatterns = [
    path('', views.publicacion, name="mis_turnos"),
]