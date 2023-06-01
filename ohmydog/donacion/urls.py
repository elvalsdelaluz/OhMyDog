from django.urls import path
from donacion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('donar/<int:donacion_id>/', views.vista_donar, name="donar"),
    path('subir_donacion', views.vista_subir_donacion, name="subir_donacion"),
    path('donaciones', views.vista_donaciones, name="donaciones"),
]