from django.shortcuts import render, redirect
from .forms import formulario_turno, Formulario_rechazado, Formulario_concluido, Formulario_aceptado
from .models import Turno
from donacion.models import Donante
from mascotas.models import EntradaLibretaSanitaria, Mascota
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.db.models import Q
from mascotas.forms import EntradaLibretaSanitariaForm

# Create your views here.
#def mis_turnos(request):

 #   return render (request, "turnos/misturnos.html")

def devolver_turno(numero):
    return "Mañana" if numero == '0' else "Tarde"


def publicacion(request):
    ##########################################################
    ###################BLOQUEO OPCION#########################
    usuario_autenticado = request.user
    if usuario_autenticado.is_authenticated and not usuario_autenticado.is_staff:
        #pregunto si tiene perros  
        tiene_perros = Mascota.objects.filter(dueño=usuario_autenticado).exists()
        if not tiene_perros:
            return redirect('alta_mascota')
    ##########################################################

    formulario=formulario_turno(user=request.user)

    turnos=Turno.objects.filter(dueño=request.user)

    if (turnos.filter(estado='Pendiente' or 'Aceptado' or '0' or '1').filter(fecha__lte=date.today()).exists()):
        turnos_vencidos=turnos.filter(estado='Pendiente' or 'Aceptado' or '0' or '1').filter(fecha__lte=date.today())
        turnos_vencidos.update(estado='5')
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
            nuevo_turno.estado='Pendiente'

            distancia_edad_turno=(nuevo_turno.fecha - nuevo_turno.mascota.fecha_nacimiento).days
            
            distancia_libreta_turno=0
            distancia_libreta_turnoB=0
            if (EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).exists()):
                if (EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='0').exists()):
                    ultima_libreta = EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='0').order_by('fecha').first()
                    distancia_libreta_turno= (date.today()-ultima_libreta.fecha).days
                if (EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='1').exists()):
                    ultima_libretaB = EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='1').order_by('fecha').first()
                    distancia_libreta_turnoB= (date.today()-ultima_libretaB.fecha).days

            """if nuevo_turno.fecha < date.today():
                error= " Por favor selecciona una fecha valida"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (nuevo_turno.fecha - date.today()).days < 1:
                error = "Por favor, solicita tu turno con al menos 24hs de antelacion"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif nuevo_turno.fecha.weekday() == 6:
                error= "Lo sentimos, no trabajamos los domingos. Por favor elegi otro dia de la semana"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})"""
            
            if (nuevo_turno.motivo== '1' and (distancia_edad_turno< 60)):
                error= "Lo sentimos, la Vacuna A solo puede aplicarse a perros mayores a dos meses"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (nuevo_turno.motivo== '2' and (distancia_edad_turno< 120)):
                error= "Lo sentimos, la Vacuna B solo puede aplicarse a perros mayores a cuatro meses"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (Turno.objects.filter(mascota=nuevo_turno.mascota).filter(estado='Pendiente') or 
                  (Turno.objects.filter(mascota=nuevo_turno.mascota).filter(estado='Aceptado'))):
                error= "Lo sentimos, tu mascota ya tiene un turno activo"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            
            elif (nuevo_turno.motivo== '1' and (distancia_edad_turno<120) and EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='0').exists() and distancia_libreta_turno<21):
                error = "Lo sentimos. El refuerzo de la Vacuna A a perros menores a 4 meses debe darse recién pasados 21 días"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            elif (nuevo_turno.motivo== '1' and EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='0').exists() and distancia_libreta_turno<365):
                error = "Lo sentimos. El refuerzo de la Vacuna A debe darse recién un año desde la ultima aplicacion"
                return render (request, 'turnos/misturnos.html',{'formulario':formulario, "error":error,'turnos':turnos})
            elif (nuevo_turno.motivo== '2' and EntradaLibretaSanitaria.objects.filter(perro=nuevo_turno.mascota).filter(motivo='1').exists() and distancia_libreta_turnoB<365):
                error = "Lo sentimos. El refuerzo de la Vacuna B debe darse recién un año desde la ultima aplicacion"
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

    turnos_pendientes=Turno.objects.filter(estado='Pendiente')|Turno.objects.filter(estado='0')

    if (turnos_pendientes.filter(fecha__lte=date.today()).exists()):
        turnos_vencidos=turnos_pendientes.filter(fecha__lte=date.today())
        turnos_vencidos.update(estado='5')
        turnos_pendientes=Turno.objects.filter(estado='Pendiente')

    turnos_vencidos=Turno.objects.filter(estado='5')

    return render(request, 'turnos/turnospendientes.html', {'turnos':turnos_pendientes, 'turnosV':turnos_vencidos})

def ver_turnos_activos(request):
    """
    for objeto in Turno.objects.all():
        print(objeto.estado)
        print(objeto.fecha)
    """
    turnos_activos=Turno.objects.filter(Q(estado='Aceptado') | Q(estado="1"))

    return render(request, 'turnos/turnosactivos.html', {'turnos':turnos_activos})

def ver_turnos_pasados(request):

    turnos_pasados=Turno.objects.filter(estado='Rechazado')|Turno.objects.filter(estado='Cancelado')

    turnos_cerrados=Turno.objects.filter(estado='Cerrado')

    return render(request, 'turnos/turnospasados.html', {'turnos':turnos_pasados,'turnos1':turnos_cerrados})

def aceptar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    def set_horario(franja):
        if franja == 'Mañana':
            return Turno.horarios[0:8]
        elif franja == 'Tarde':
            return Turno.horarios[8:16]

    formu = Formulario_aceptado(set_horario(devolver_turno(turno.franjaHoraria)))

    if request.method=='POST':

        formu = Formulario_aceptado(set_horario(devolver_turno(turno.franjaHoraria)),data=request.POST)
        if formu.is_valid():

            if (Turno.objects.filter(fecha=turno.fecha).filter(estado="Aceptado").filter(hora=formu.cleaned_data['hora']).exists()):
                error = "Lo sentimos. Ya tenes un turno reservado para esta hora"
                return render(request, 'turnos/formulario_aceptacion.html', {'formulario':formu, 'error':error, 'turno':turno})

            turno.hora = formu.cleaned_data['hora']

            turno.estado='Aceptado'
            turno.save()

            send_mail(
                "Turno aceptado", 
                f"El turno ha sido aceptado.\n Motivo del turno: {turno.get_motivo_display()}\n Nombre del perro:  {turno.mascota}\n Franja horaria: {turno.get_franjaHoraria_display()}\n Hora:{turno.get_hora_display()}\n Fecha: {turno.fecha}", 
                "ohmydog.veterinariacanina@gmail.com", 
                [turno.dueño.email, "ohmydog.veterinariacanina@gmail.com"], 
                fail_silently=False
            )


        return redirect('/mis_turnos/turnos_pendientes/?valido')
    
    return render(request, 'turnos/formulario_aceptacion.html', {'formulario':formu, 'turno':turno})
    

def cancelar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    if (turno.fecha - date.today()).days <=1:
        
        return redirect('/mis_turnos/?novalido')

    turno.estado='Cancelado'
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
            turno.estado='Rechazado'
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
    
    return render(request, 'turnos/formulario_rechazo.html', {'formulario':formu, 'turno':turno})



def ver_motivo_rechazo(request, motivo):
    return render(request, 'turnos/informacion_rechazo.html', {'motivo': motivo})



def concluir_turno(request, pk):
    motivos_actualizacion_libreta=["Vacuna A", "Vacuna B", "Desparacitacion", "1", "2", "3"]

    turno = get_object_or_404(Turno, pk=pk)

    """if (turno.fecha > date.today()):
                return redirect ('/mis_turnos/turnos_activos/?novalido')"""

    formu = Formulario_concluido()

    monto_descuento=0
    if (turno.dueño.es_donante):
        monto_descuento=turno.dueño.descuento_acumulado
    

    if request.method=='POST':
        formu = Formulario_concluido(data=request.POST)
        if formu.is_valid():
            observaciones = formu.cleaned_data['observaciones']
            monto = formu.cleaned_data['monto']
            turno.observaciones = observaciones
            if (turno.dueño.es_donante):
                monto_descuento=turno.dueño.descuento_acumulado
                if (monto<monto_descuento):
                    turno.dueño.descuento_acumulado=turno.dueño.descuento_acumulado-monto
                    monto=0
                else:
                    turno.monto = monto - monto_descuento
                    turno.dueño.descuento_acumulado=0
                    turno.dueño.es_donante=False
                turno.dueño.save()
                turno.descuento=True
            else:
                turno.monto=monto
                turno.descuento=False
            turno.estado='Cerrado'
            turno.save()

        if not turno.motivo in motivos_actualizacion_libreta:
            return redirect ('/mis_turnos/turnos_activos/?valido')
        else:
            formulario_libreta= EntradaLibretaSanitariaForm()
            if request.method=='POST':
            #Al parecer el botón utilizado es mucho muy importante. Dependiendo de que botón sea entra o no.
            #<input class="btn btn-success" type="submit" value="Confirmar"  style="margin-right: 10px;">
                formulario_libreta = EntradaLibretaSanitariaForm(data=request.POST)
                if formulario_libreta.is_valid():
                    entrada_nueva = EntradaLibretaSanitaria()
                    entrada_nueva.fecha = turno.fecha
                    entrada_nueva.motivo = turno.motivo
                    entrada_nueva.perro = turno.mascota
                    entrada_nueva.peso = formulario_libreta.cleaned_data['peso']
                    if turno.motivo =="Desparasitacion":
                        entrada_nueva.cantidad_desparasitario = formulario_libreta.cleaned_data['cantidad_desparasitario']
                    else:
                        entrada_nueva.cantidad_desparasitario=0
                    entrada_nueva.save()
                    return redirect ('/mis_turnos/turnos_activos/?valido')
            return render(request, 'turnos/actualizar_libreta_sanitaria.html', {'formulario_libreta':formulario_libreta, 'info_turno':turno})

        #return redirect ('/mis_turnos/turnos_activos/?valido')
    
    return render(request, 'turnos/formulario_cierre.html', {'formulario':formu, 'turno':turno, 'donante':turno.dueño.es_donante, 'descuento':monto_descuento, 'actualizar_libreta':motivos_actualizacion_libreta})

def ver_historia_turno(request, pk):

    turno = get_object_or_404(Turno, pk=pk)

    return render(request, 'turnos/historia_turno.html', {'turno': turno})


"""

#ESTO NO ME FUNCIONO, YO INTENTE QUE SEA LEGIBLE, NO ME JUZGEN SOY HUMANA
def actualizar_libreta_sanitaria(request, turno_id): 
    info_turno = Turno.objects.get(id=turno_id)
    formulario_libreta= EntradaLibretaSanitariaForm()

    if request.method=='POST':
        #Al parecer el botón utilizado es mucho muy importante. Dependiendo de que botón sea entra o no.
        #<input class="btn btn-success" type="submit" value="Confirmar"  style="margin-right: 10px;">
        formulario_libreta = EntradaLibretaSanitariaForm(data=request.POST)
        if formulario_libreta.is_valid():
            entrada_nueva = EntradaLibretaSanitaria()
            entrada_nueva.fecha = info_turno.fecha
            entrada_nueva.motivo = info_turno.motivo
            entrada_nueva.perro = info_turno.mascota
            entrada_nueva.peso = formulario_libreta.cleaned_data['peso']
            #entrada_nueva.cantidad_desparacitario = formulario_libreta.cleaned_data['cantidad_desparacitario']
            print(entrada_nueva.save())
            print("que pasooooooooooooooooo")
        return redirect ('/mis_turnos/turnos_activos/?valido')

    return render(request, 'turnos/actualizar_libreta_sanitaria.html', {'formulario_libreta':formulario_libreta, 'info_turno':info_turno})
"""