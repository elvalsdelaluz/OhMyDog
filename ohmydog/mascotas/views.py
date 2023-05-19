from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MascotaForm
from .models import Mascota
from autenticacion.models import Cuenta
from datetime import date

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
            if (mascota_form.cleaned_data['fecha_nacimiento'])>date.today():
                error = "No puedes ingresar una fecha de nacimiento posterior al dia de hoy"
                return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form,'error':error})
            else:
                if (Mascota.objects.filter(dueño=request.user).filter(nombre=mascota_form.cleaned_data['nombre'])):
                    error = "Ya agregaste a esa mascota a nuestra base de datos"
                    return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form,'error':error})
                else:
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
                        email = request.GET.get('email') 
                        dueño = Cuenta.objects.get(email=email)
                        nueva_mascota.dueño= dueño
                        nueva_mascota.save()
                    else:
                        nueva_mascota.dueño=request.user
                        nueva_mascota.save()
                        mascota_form = MascotaForm()
                        return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form, 'mensaje':"ok"})
        
    return render(request, 'mascotas/alta_mascota.html', {'form':mascota_form})
