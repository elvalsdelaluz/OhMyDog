from django.urls import path
from contactoPaseadoresCuidadores import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.contactoPaseadoresCuidadores, name="contactoPaseadoresCuidadores"),
    path('alta_proveedor', views.alta_proveedor, name='alta_proveedor'),
    path('bajar_proveedor/<int:proveedor_id>/', views.bajar_proveedor, name="bajar_proveedor"),
    path('baja_temporal/<int:proveedor_id>/', views.baja_temporaria, name="baja_temporal"),
    path('resubir_proveedor/<int:proveedor_id>/',views.resubir_proveedor, name='resubir_proveedor'),
]
