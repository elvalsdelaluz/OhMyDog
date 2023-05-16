from django.urls import path
from .views import alta_mascota

urlpatterns=[
    path('alta_mascota', alta_mascota, name="alta_mascota"),
]
