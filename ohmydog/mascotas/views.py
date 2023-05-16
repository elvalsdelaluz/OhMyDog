from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MascotaForm
# Create your views here.


def alta_mascota(request):
    mascota_form = MascotaForm()
    if request.method == 'POST':
        mascota_form = MascotaForm(data=request.POST)

        if mascota_form.is_valid():
            mascota_form.save()
            return redirect(reverse('mascota')+'?ok')
        else:
            return redirect(reverse('mascota'+'?error'))

    return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form})
