from django.shortcuts import render
from .forms import formulario_turno
from .models import Turno
from django.contrib.auth import get_user_model


# Create your views here.
#def mis_turnos(request):

 #   return render (request, "turnos/misturnos.html")

def publicacion(request):

    formulario=formulario_turno()

    turnos=Turno.objects.filter()

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

            formulario=formulario_turno()

            return render (request, 'turnos/misturnos.html',{'formulario':formulario, "mensaje":"ok",'turnos':turnos})
        
    return render(request, 'turnos/misturnos.html', {'formulario':formulario,'turnos':turnos})