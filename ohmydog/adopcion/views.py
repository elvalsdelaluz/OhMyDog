from django.shortcuts import render
from adopcion.models import Adopcion

def adopcion (request):
    return render(request, "adopcion/adopcion.html", {"adopciones":Adopcion.objects.all()})
