from django.urls import path
from adopcion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.adopcion, name="adopcion"),
    path('solicitud', views.publicacion, name="solicitud"),
    path('contactar/<int:adopcion_id>/', views.datos_adopcion, name="contactar"),
    path('editar_informacion/<int:adopcion_id>/', views.editar_perro_adopcion, name="editar_informacion"),
]