from django.urls import path,re_path
from donacion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('donar/<int:donacion_id>/', views.vista_donar, name="donar"),
    path('subir_donacion', views.vista_subir_donacion, name="subir_donacion"),
    path('donaciones', views.vista_donaciones, name="donaciones"),
    path('pago_realizado', views.vista_pago_realizado, name="pago_realizado"),
    path('ver_registro/<int:donacion_id>/', views.ver_registro, name="ver_registro")
]