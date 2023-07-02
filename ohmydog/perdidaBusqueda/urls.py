from django.urls import path
from perdidaBusqueda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.mostrar_perros_perdidos, name="mostrar_perros_perdidos"),
    path('publicar_perro_perdido', views.publicar_perro_perdido, name="publicar_perro_perdido"),
    path('cambiar_a_localizado/<int:perdido_id>/', views.cambiar_a_localizado, name="cambiar_a_localizado"),
    path('eliminar_publicacion/<int:perdido_id>/', views.eliminar_publicacion, name="eliminar_publicacion"),
]