from django.urls import path
from perdidaBusqueda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.mostrar_perros_perdidos, name="mostrar_perros_perdidos"),
    path('publicar_perro_perdido', views.publicar_perro_perdido, name="publicar_perro_perdido"),
]