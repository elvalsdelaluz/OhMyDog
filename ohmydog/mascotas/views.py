from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MascotaForm
from .models import Mascota, EntradaLibretaSanitaria
from autenticacion.models import Cuenta
from datetime import date
from turnos.models import Turno
# Create your views here.

def mascota_registrada (user, nombre_mascota): 
    """Si el usuario ya tiene una publicación con nombre, fecha y sexo 
       la función devuelve true
    """ 
    existe_publicacion=False
    publicaciones_del_usuario= Mascota.objects.filter(dueño=user)

    if publicaciones_del_usuario.exists(): #Si el querySet no esta vacio
        #Verifico para cada publicacion el campo nombre
        #En caso de encontrar una igual modifico el valor de existe_publicacion
        for publicacion in publicaciones_del_usuario:
            if publicacion.nombre == nombre_mascota:
                existe_publicacion=True
                break
    return existe_publicacion



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
    print("HOALDFASJKF")
    print(mascota_id)
    objeto_mascota=Mascota.objects.get(id=mascota_id)
    print(EntradaLibretaSanitaria.objects.filter(perro=objeto_mascota))
    mi_libreta=EntradaLibretaSanitaria.objects.filter(perro=objeto_mascota)
    
    return render(request, 'mascotas/ver_libreta_sanitaria.html', {'mi_libreta':mi_libreta, 'nombre_mascota':objeto_mascota.nombre})


def no_hubo_cambios(mi_mascota, formulario_mascota):
    estado= mi_mascota.nombre == formulario_mascota.cleaned_data['nombre'] and mi_mascota.fecha_nacimiento == formulario_mascota.cleaned_data['fecha_nacimiento'] and mi_mascota.sexo == formulario_mascota.cleaned_data['sexo'] and mi_mascota.raza == formulario_mascota.cleaned_data['raza'] and mi_mascota.observaciones == formulario_mascota.cleaned_data['observaciones']
    print (estado)
    print ("hadfaskjdfh")
    return estado

def formulario_mascota_inicial(mi_mascota):
    formulario_mascota = MascotaForm(initial={
            'nombre': mi_mascota.nombre,
            'fecha_nacimiento': mi_mascota.fecha_nacimiento,
            'sexo': mi_mascota.sexo,
            'raza': mi_mascota.raza,
            'observaciones': mi_mascota.observaciones
        })
    return formulario_mascota

def guardar_datos(mi_mascota, formulario_mascota, dueño):
    mi_mascota.dueño=dueño
    mi_mascota.nombre = formulario_mascota.cleaned_data['nombre']
    mi_mascota.fecha_nacimiento = formulario_mascota.cleaned_data['fecha_nacimiento']
    mi_mascota.sexo = formulario_mascota.cleaned_data['sexo']
    mi_mascota.raza = formulario_mascota.cleaned_data['raza']
    mi_mascota.observaciones = formulario_mascota.cleaned_data['observaciones']
    mi_mascota.save()

def editar_mi_mascota(request, mascota_id):
    mi_mascota = Mascota.objects.get(id=mascota_id)
    
    if request.method=='POST': #Toco confirmar
        formulario_mascota = MascotaForm(data=request.POST)
        if formulario_mascota.is_valid():
            if  no_hubo_cambios(mi_mascota, formulario_mascota):
                return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota_inicial(mi_mascota)})
            elif mi_mascota.nombre != formulario_mascota.cleaned_data['nombre']:
                if mascota_registrada(request.user, formulario_mascota.data['nombre']):
                    #Agregar un mensaje error en el formulario html, cambiar el contexto mensaje por el valor error
                    error_ya_publicado="¡Ya tiene una mascota con ese nombre!"
                    return render (request, 'mascotas/editar_mi_mascota.html',{'formulario_mascota':formulario_mascota, "mensaje2":error_ya_publicado})
                else:
                    #guardar datos   
                    guardar_datos(mi_mascota, formulario_mascota, request.user) 
                    mensaje="Los cambios se han guardado correctamente."
                    return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota, "mensaje": mensaje})
            else:
               # guardar datos
                guardar_datos(mi_mascota, formulario_mascota, request.user) 
                mensaje="Los cambios se han guardado correctamente."
                return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota, "mensaje": mensaje})

        return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota})  
    
    return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota_inicial(mi_mascota)})


"""
def editar_mi_mascota(request, mascota_id):
    mi_mascota = Mascota.objects.get(id=mascota_id)
    
    if request.method=='POST':
        formulario_mascota = MascotaForm(data=request.POST)
        if formulario_mascota.is_valid():
            #Verifico que no tenga una mascota en adopción con el mismo nombre
            nombre_ingresado = formulario_mascota.cleaned_data['nombre']
            if nombre_ingresado != mi_mascota.nombre:
                if mascota_registrada(request.user, formulario_mascota.data['nombre']):
                    #Agregar un mensaje error en el formulario html, cambiar el contexto mensaje por el valor error
                    error_ya_publicado="¡Ya tiene una mascota con ese nombre!"
                    return render (request, 'mascotas/editar_mi_mascota.html',{'formulario_mascota':formulario_mascota, "mensaje2":error_ya_publicado})
                else:
                    mi_mascota.dueño=request.user
                    mi_mascota.nombre = formulario_mascota.cleaned_data['nombre']
                    mi_mascota.fecha_nacimiento = formulario_mascota.cleaned_data['fecha_nacimiento']
                    mi_mascota.sexo = formulario_mascota.cleaned_data['sexo']
                    mi_mascota.raza = formulario_mascota.cleaned_data['raza']
                    mi_mascota.observaciones = formulario_mascota.cleaned_data['observaciones']
                    mi_mascota.save()
                    mensaje="Los cambios se han guardado correctamente."
                    return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota, "mensaje": mensaje})
            else:
                mi_mascota.dueño=request.user
                mi_mascota.nombre = formulario_mascota.cleaned_data['nombre']
                mi_mascota.fecha_nacimiento = formulario_mascota.cleaned_data['fecha_nacimiento']
                mi_mascota.sexo = formulario_mascota.cleaned_data['sexo']
                mi_mascota.raza = formulario_mascota.cleaned_data['raza']
                mi_mascota.observaciones = formulario_mascota.cleaned_data['observaciones']
                mi_mascota.save()
                mensaje="Los cambios se han guardado correctamente."
                ..return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota, "mensaje": mensaje})

    else:
        formulario_mascota = MascotaForm(initial={
            'nombre': mi_mascota.nombre,
            'fecha_nacimiento': mi_mascota.fecha_nacimiento,
            'sexo': mi_mascota.sexo,
            'raza': mi_mascota.raza,
            'observaciones': mi_mascota.observaciones
        })
        return render(request, 'mascotas/editar_mi_mascota.html', {'formulario_mascota': formulario_mascota})

"""