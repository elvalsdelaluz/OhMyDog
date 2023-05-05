from django.urls import path
from adopcion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.adopcion, name="adopcion"),
]