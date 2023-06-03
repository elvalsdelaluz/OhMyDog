from django.urls import path
from adopcion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.adopcion, name="adopcion"),
    path('solicitud', views.publicacion, name="solicitud"),
    path('contactar/<int:adopcion_id>/', views.datos_adopcion, name="contactar"),
    path('editar_post_adopcion/<int:adopcion_id>/', views.editar_post_adopcion, name="editar_post_adopcion"),
    path('cerrar_post/<int:adopcion_id>/', views.cerrar_post, name="cerrar_post"),
    path('bajar_post/<int:adopcion_id>/', views.bajar_post, name="bajar_post"),
]