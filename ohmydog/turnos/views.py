from django.shortcuts import render
from .forms import formulario_turno
from .models import Turno
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


# Create your views here.
#def mis_turnos(request):

 #   return render (request, "turnos/misturnos.html")

def publicacion(request):

    formulario=formulario_turno()

    turnos=Turno.objects.filter(dueño=request.user)

    if request.method=='POST':
        formulario=formulario_turno(data=request.POST)
        if formulario.is_valid():
            #Aca hay que hacerlo andar
            nuevo_turno=Turno()
            nuevo_turno.dueño=request.user
            nuevo_turno.motivo=formulario.cleaned_data['motivo']
            nuevo_turno.mascota=formulario.cleaned_data['mascota']
            nuevo_turno.franja=formulario.cleaned_data['franja']
            nuevo_turno.fecha=formulario.cleaned_data['fecha']
            nuevo_turno.estado=Turno.estados[0][1]

            nuevo_turno.save()


            ##despues hacer un switch para que en vez de que "diga motivo de turno: 1" diga "motivo de turno: Vacuna A"
            send_mail(
                "Turno solicitado", 
                f"Se ha registrado la solicitud de turno con la siguiente informacion:\n Motivo del turno: {nuevo_turno.motivo}\n Nombre del perro:  {nuevo_turno.mascota}\n Franja horaria: {nuevo_turno.franja}\n Fecha: {nuevo_turno.fecha}\n Estado del turno: {nuevo_turno.estado}", 
                "ohmydog.veterinariacanina@gmail.com", 
                [request.user.email, "ohmydog.veterinariacanina@gmail.com"], 
                fail_silently=False
            )

            formulario=formulario_turno()

            return render (request, 'turnos/misturnos.html',{'formulario':formulario, "mensaje":"ok",'turnos':turnos})
        
    return render(request, 'turnos/misturnos.html', {'formulario':formulario,'turnos':turnos})

def ver_turnos_pendientes(request):

    turnos_pendientes=Turno.objects.filter(estado='Pendiente')

    return render(request, 'turnos/turnospendientes.html', {'turnos':turnos_pendientes})

def ver_turnos_activos(request):

    turnos_activos=Turno.objects.filter(estado=Turno.estados[1][1])

    return render(request, 'turnos/turnosactivos.html', {'turnos':turnos_activos})

def ver_turnos_pasados(request):

    turnos_pasados=Turno.objects.filter(estado='2')|Turno.objects.filter(estado='3')|Turno.objects.filter(estado='4')

    return render(request, 'turnos/turnospasados.html', {'turnos':turnos_pasados})

def aceptar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    turno.estado=Turno.estados[1][1]
    turno.save()


    turnos_pendientes=Turno.objects.filter(estado='Pendiente')

    return render(request, 'turnos/turnospendientes.html', {'turnos':turnos_pendientes})

