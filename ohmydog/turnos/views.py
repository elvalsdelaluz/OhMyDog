from django.shortcuts import render, redirect
from .forms import formulario_turno, Formulario_rechazado
from .models import Turno
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from datetime import date, timedelta


# Create your views here.
#def mis_turnos(request):

 #   return render (request, "turnos/misturnos.html")

def devolver_turno(numero):
    return "Mañana" if numero == '0' else "Tarde"


def publicacion(request):

    formulario=formulario_turno(user=request.user)

    turnos=Turno.objects.filter(dueño=request.user)


    if request.method=='POST':
        formulario=formulario_turno(data=request.POST, user=request.user)
        if formulario.is_valid():
            #Aca hay que hacerlo andar
            
            nuevo_turno=Turno()
            nuevo_turno.dueño=request.user
            nuevo_turno.motivo=formulario.cleaned_data['motivo']
            nuevo_turno.mascota=formulario.cleaned_data['mascota']
            nuevo_turno.franjaHoraria=formulario.cleaned_data['franja']
            nuevo_turno.fecha=formulario.cleaned_data['fecha']
            nuevo_turno.estado=Turno.estados[0][1]

            """if nuevo_turno.fecha < date.today():
                error= " Por favor selecciona una fecha valida"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (nuevo_turno.fecha - date.today()).days < 1:
                error = "Por favor, solicita tu turno con al menos 24hs de antelacion"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif nuevo_turno.fecha.weekday() == 6:
                error= "Lo sentimos, no trabajamos los domingos. Por favor elegi otro dia de la semana"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})"""
            
            if (nuevo_turno.motivo== '1' and (((nuevo_turno.fecha.year - nuevo_turno.mascota.fecha_nacimiento.year)*12) 
                                    + (nuevo_turno.fecha.month - nuevo_turno.mascota.fecha_nacimiento.month)< 2)):
                error= "Lo sentimos, la Vacuna A solo puede aplicarse a perros mayores a dos meses"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (nuevo_turno.motivo== '2' and (((nuevo_turno.fecha.year - nuevo_turno.mascota.fecha_nacimiento.year)*12) 
                                    + (nuevo_turno.fecha.month - nuevo_turno.mascota.fecha_nacimiento.month)< 4)):
                error= "Lo sentimos, la Vacuna B solo puede aplicarse a perros mayores a cuatro meses"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (Turno.objects.filter(mascota=nuevo_turno.mascota).filter(estado='Pendiente') or 
                  (Turno.objects.filter(mascota=nuevo_turno.mascota).filter(estado='Activo'))):
                error= "Lo sentimos, tu mascota ya tiene un turno activo"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            else:

                nuevo_turno.save()


                send_mail(
                    "Turno solicitado", 
                    f"Se ha registrado la solicitud de turno con la siguiente informacion:\n Motivo del turno: {nuevo_turno.get_motivo_display()}\n Nombre del perro:  {nuevo_turno.mascota}\n Franja horaria: {nuevo_turno.get_franjaHoraria_display()}\n Fecha: {nuevo_turno.fecha}\n Estado del turno: Pendiente", 
                    "ohmydog.veterinariacanina@gmail.com", 
                    [request.user.email, "ohmydog.veterinariacanina@gmail.com"], 
                    fail_silently=False
                )

            

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

    send_mail(
                "Turno aceptado", 
                f"El turno ha sido aceptado.\n Motivo del turno: {turno.get_motivo_display()}\n Nombre del perro:  {turno.mascota}\n Franja horaria: {turno.get_franjaHoraria_display()}\n Fecha: {turno.fecha}", 
                "ohmydog.veterinariacanina@gmail.com", 
                [turno.dueño.email, "ohmydog.veterinariacanina@gmail.com"], 
                fail_silently=False
            )
    turnos_pendientes=Turno.objects.filter(estado='Pendiente')

    return render(request, 'turnos/turnospendientes.html', {'turnos':turnos_pendientes})

def cancelar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    if (turno.fecha - date.today()).days <=1:
        
        return redirect('/mis_turnos/?novalido')

    turno.estado=Turno.estados[3][1]
    turno.save()

    send_mail(
                "Turno cancelado", 
                f"El turno ha sido cancelado.\n Motivo del turno: {turno.get_motivo_display()}\n Nombre del perro:  {turno.mascota}\n Franja horaria: {turno.get_franjaHoraria_display()}\n Fecha: {turno.fecha}", 
                "ohmydog.veterinariacanina@gmail.com", 
                [turno.dueño.email, "ohmydog.veterinariacanina@gmail.com"], 
                fail_silently=False
            )

    return redirect ('/mis_turnos/?valido')



def rechazar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    formu = Formulario_rechazado()

    if request.method=='POST':

        formu = Formulario_rechazado(data=request.POST)
        if formu.is_valid():

            motivo_rechazo = formu.cleaned_data['motivo_rechazo']

            turno.motivo_rechazo = motivo_rechazo
            turno.estado=Turno.estados[2][1]
            turno.save()

            send_mail(
                "Turno rechazado", 
                f"El turno ha sido cancelado.\n Motivo del turno: {turno.get_motivo_display()}\n Nombre del perro:  {turno.mascota}\n Franja horaria: {turno.get_franjaHoraria_display()}\n Fecha: {turno.fecha}", 
                "ohmydog.veterinariacanina@gmail.com", 
                [turno.dueño.email, "ohmydog.veterinariacanina@gmail.com"], 
                fail_silently=False
            )


            turnos_pendientes=Turno.objects.filter(estado='Pendiente')

        return render(request, 'turnos/turnospendientes.html', {'turnos':turnos_pendientes})
    
    return render(request, 'turnos/formulario_rechazo.html', {'formulario':formu})



def ver_motivo_rechazo(request, motivo):
    return render(request, 'turnos/informacion_rechazo.html', {'motivo': motivo})