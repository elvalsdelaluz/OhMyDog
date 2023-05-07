from django.urls import path
from veterinariasDeTurno import views

urlpatterns = [
    path('', views.veterinariasDeTurno, name="veterinariasDeTurno"),
]