from django.shortcuts import render, redirect
from adopcion.models import Adopcion
from .forms import formulario_Adopcion, FormularioDatosAdopcionLogueado, FormularioDatosAdopcionNoUsuario
from django.core.mail import send_mail

def adopcion (request):
    adopciones = Adopcion.objects.all()
    return render(request, "adopcion/adopcion.html", {"adopciones":adopciones})


def publicacion(request):

    formulario_adopcion=formulario_Adopcion()

    if request.method=='POST':
        formulario_adopcion=formulario_Adopcion(data=request.POST)
        if formulario_adopcion.is_valid():
            #Aca hay que hacerlo andar
            nueva_adopcion=Adopcion()
            nueva_adopcion.dueño=request.user
            nueva_adopcion.nombre=formulario_adopcion.cleaned_data['nombre']
            nueva_adopcion.sexo=formulario_adopcion.cleaned_data['sexo']
            nueva_adopcion.edad=formulario_adopcion.cleaned_data['fecha_nacimiento']
            nueva_adopcion.tamaño=formulario_adopcion.cleaned_data['tamaño']
            nueva_adopcion.estado=Adopcion.Estado[0][1]
            nueva_adopcion.comentarios=formulario_adopcion.cleaned_data['comentarios']

            nueva_adopcion.save()

            formulario_adopcion=formulario_Adopcion()

            return render (request, 'adopcion/adopcion/solicitud.html',{'formulario':formulario_adopcion, "mensaje":"ok"})
        
    return render(request, 'adopcion/adopcion/solicitud.html', {'formulario':formulario_adopcion})



def datos_adopcion(request, adopcion_id):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = FormularioDatosAdopcionLogueado(request.POST)
            if form.is_valid():
                motivo = form.cleaned_data['motivo']
                adopcion = Adopcion.objects.get(id=adopcion_id)
                send_mail(
                    "Solicitud de adopción",
                    f"{request.user.nombre} se quiere contactar para adoptar el perro que publicaste.\n Esta es su información de contacto:\n *Numero: {request.user.numero}\n *Email: {request.user.email} \n Motivo: {motivo}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", request.user.email, adopcion.dueño.email]
                )
                return redirect("home")

        form = FormularioDatosAdopcionLogueado()
        return render(request, "adopcion/contactar.html", {'formulario': form})
    else:
        if request.method == 'POST':
            form = FormularioDatosAdopcionNoUsuario(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                nombre = form.cleaned_data['nombre']
                numero = form.cleaned_data['numero']
                motivo = form.cleaned_data['motivo']
                adopcion = Adopcion.objects.get(id=adopcion_id)
                send_mail(
                    "Solicitud de adopción",
                    f"{nombre} se quiere contactar para adoptar el perro que publicaste.\n Esta es su información de contacto:\n *Numero: {numero}\n *Email: {email} \n Motivo: {motivo}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", email, adopcion.dueño.email]
                )
                return redirect("home")

        form = FormularioDatosAdopcionNoUsuario()
        return render(request, "adopcion/contactar.html",{'formulario':form})


def editar_perro_adopcion(request, adopcion_id):    
    posteo = Adopcion.objects.get(id=adopcion_id)

    if request.method=='POST':
        formulario_adopcion = formulario_Adopcion(data=request.POST)
        if formulario_adopcion.is_valid():
            posteo.dueño=request.user
            posteo.nombre = formulario_adopcion.cleaned_data['nombre']
            posteo.fecha_nacimiento = formulario_adopcion.cleaned_data['fecha_nacimiento']
            posteo.sexo = formulario_adopcion.cleaned_data['sexo']
            posteo.tamaño = formulario_adopcion.cleaned_data['tamaño']
            posteo.comentarios = formulario_adopcion.cleaned_data['comentarios']
            posteo.estado=Adopcion.Estado[0][1]
            posteo.save()
            return redirect("adopcion") #modificar para que lo redirija a donde estan los perros publicados "adopcion"

    else:
        formulario_adopcion = formulario_Adopcion(initial={
            'nombre': posteo.nombre,
            'fecha_nacimiento': posteo.fecha_nacimiento,
            'sexo': posteo.sexo,
            'tamaño': posteo.tamaño,
            'comentarios': posteo.comentarios
        })
        return render(request, 'adopcion/editar_post.html', {'formulario_adopcion': formulario_adopcion})



def cerrar_post(request, adopcion_id): #mas adelante hacer que le pregunte al usuario si quiere o no realizar la operacion (paso intermedio)
    posteo = Adopcion.objects.get(id=adopcion_id)
    posteo.estado = Adopcion.Estado[1][1]
    posteo.save()   
    return redirect("adopcion")