from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MascotaForm
from .models import Mascota, EntradaLibretaSanitaria
from autenticacion.models import Cuenta
from datetime import date
from turnos.models import Turno
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


def ver_mis_mascotas(request):
    """
    Filtro las mascotas del usuario que inicio sesión
    """
    mascotas_registradas= Mascota.objects.filter(dueño=request.user)
    print(request.user)
    for mascota in mascotas_registradas:
        print (mascota.nombre)
    return render(request, 'mascotas/ver_mis_mascotas.html', {'mascotas_registradas': mascotas_registradas})


def ver_historial_turnos(request, mascota_id):
    """
    Necesito recibir a la mascota y filtrar.
    """
    mi_historial=Turno.objects.filter(mascota=mascota_id)
    nombre_mascota=Mascota.objects.get(id=mascota_id)
    """
    for historia in mi_historial:
        print(historia.mascota)
        print (historia.fecha)
    """
    return render(request, 'mascotas/ver_historial_turnos.html', {'mi_historial':mi_historial, 'nombre_mascota':nombre_mascota.nombre})

def ver_libreta_sanitaria(request, mascota_id):
    """
       Guardar la fecha, el peso actual del perro y en caso de que sea vacunación, 
       el tipo de vacuna, si es desparasitación, la cantidad de antiparasitario. 
    """
    mi_libreta=EntradaLibretaSanitaria.objects.filter(mascota=mascota_id)
    nombre_mascota=Mascota.objects.get(id=mascota_id)
    return render(request, 'mascotas/ver_libreta_sanitaria.html', {'mi_libreta':mi_libreta, 'nombre_mascota':nombre_mascota.nombre})


