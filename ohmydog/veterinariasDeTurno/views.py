from django.shortcuts import render
from veterinariasDeTurno.models import VeterinariasDeTurno

def veterinariasDeTurno (request):
    veterinariasDeTurno = VeterinariasDeTurno.objects.all()
    return render(request, "veterinariasDeTurno/veterinariasDeTurno.html", {"veterinariasDeTurno": veterinariasDeTurno})
