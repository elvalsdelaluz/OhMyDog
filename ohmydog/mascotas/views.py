from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MascotaForm
from .models import Mascota
from autenticacion.models import Cuenta

# Create your views here.

def verificacion_email(email_ingresado):
    #existe_producto = Producto.objects.filter(codigo='ABC123').exists()
    existe_cuenta=Cuenta.objects.filter(email=email_ingresado).exists()
    if existe_cuenta:
        return Cuenta.objects.get(email=email_ingresado)
    else:
        return None


def alta_mascota(request):
    mascota_form = MascotaForm()
    if request.method == 'POST':
        mascota_form = MascotaForm(data=request.POST)
        
        if mascota_form.is_valid():
            nueva_mascota=Mascota()
    
            nueva_mascota.nombre=mascota_form.cleaned_data['nombre']
            nueva_mascota.raza=mascota_form.cleaned_data['raza']
            nueva_mascota.sexo=mascota_form.cleaned_data['sexo']
            nueva_mascota.fecha_nacimiento=mascota_form.cleaned_data['fecha_nacimiento']      
            nueva_mascota.observaciones=mascota_form.cleaned_data['observaciones']
            #En caso de que sea el veterinario el que haga el alta deberia 
            #haberme guardado el usuario que acaba de registrar y settear con ese user (parece medio jede esto)
            #En caso que no sea el veterinario deberia settear el dueño con el user que inicio sesion
            #nueva_mascota.dueño=request.user
            if request.user.is_staff:
                #Tengo que recuperar al usuario que acaba de registrar el veterinario
                dueño = verificacion_email(request.POST.get('dueño'))
                if dueño == None:
                    mensaje_error="El email ingresado no pertenece a una cuenta registrada"
                    return render(request, 'mascotas/alta_mascota_fallida.html', {'mensaje':mensaje_error})
                else:
                    nueva_mascota.dueño= dueño
                    nueva_mascota.save()
            else:
                nueva_mascota.dueño=request.user
                nueva_mascota.save()
                mascota_form = MascotaForm()
                return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form})
        
    return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form})
