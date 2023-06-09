from django.shortcuts import render, redirect
from adopcion.models import Adopcion
from .forms import formulario_Adopcion, FormularioDatosAdopcionLogueado, FormularioDatosAdopcionNoUsuario
from django.core.mail import send_mail

from datetime import datetime, date



def adopcion (request):
    '''Se muestra la plantilla adopcion.html'''
    adopciones = Adopcion.objects.all()
    return render(request, "adopcion/adopcion.html", {"adopciones":adopciones})

def ya_esta_publicado(user, nombre_mascota): 
    """Si el usuario ya tiene una publicación con nombre, fecha y sexo 
       la función devuelve true
    """ 
    existe_publicacion=False
    publicaciones_del_usuario= Adopcion.objects.filter(dueño=user)

    if publicaciones_del_usuario.exists(): #Si el querySet no esta vacio
        #Verifico para cada publicacion el campo nombre
        #En caso de encontrar una igual modifico el valor de existe_publicacion
        for publicacion in publicaciones_del_usuario:
            print(publicacion)#sacar
            print(publicacion.nombre)#sacar
            print(nombre_mascota)#sacar
            if publicacion.nombre == nombre_mascota:
                existe_publicacion=True
                break
    return existe_publicacion


def publicacion(request):
    '''Se procesa la plantilla solicitud.html'''
    formulario_adopcion=formulario_Adopcion()

    if request.method=='POST':
        formulario_adopcion=formulario_Adopcion(data=request.POST)
       
        if formulario_adopcion.is_valid():
            if ya_esta_publicado(request.user, formulario_adopcion.cleaned_data['nombre']):
                #Agregar un mensaje error en el formulario html, cambiar el contexto mensaje por el valor error
                error_ya_publicado="¡Ya tiene publicada una mascota con ese nombre!"
                return render (request, 'adopcion/adopcion/solicitud.html',{'formulario':formulario_adopcion, "mensaje2":error_ya_publicado})
            else:
                #Aca hay que hacerlo andar
                nueva_adopcion=Adopcion()
                nueva_adopcion.dueño=request.user
                nueva_adopcion.nombre=formulario_adopcion.cleaned_data['nombre']
                nueva_adopcion.sexo=formulario_adopcion.cleaned_data['sexo']
                nueva_adopcion.fecha_nacimiento=formulario_adopcion.cleaned_data['fecha_nacimiento']
                nueva_adopcion.tamaño=formulario_adopcion.cleaned_data['tamaño']
                nueva_adopcion.estado=Adopcion.Estado[0][1]
                nueva_adopcion.comentarios=formulario_adopcion.cleaned_data['comentarios']

                nueva_adopcion.save()

                formulario_adopcion=formulario_Adopcion()

                return render (request, 'adopcion/adopcion/solicitud.html',{'formulario':formulario_adopcion, "mensaje":"ok"})
        
    return render(request, 'adopcion/adopcion/solicitud.html', {'formulario':formulario_adopcion})


def datos_adopcion(request, adopcion_id):
    '''Se procesa la plantilla contactar.html'''
    user = request.user
    form = FormularioDatosAdopcionLogueado()
    if user.is_authenticated:
        if request.method == 'POST':
            form = FormularioDatosAdopcionLogueado(request.POST)
            if form.is_valid():
                motivo = form.cleaned_data['motivo']
                adopcion = Adopcion.objects.get(id=adopcion_id)
                send_mail(
                    "Solicitud de adopción",
                    f"{request.user.nombre} se quiere contactar para adoptar a {adopcion.nombre}.\n Esta es su información de contacto:\n *Numero: {request.user.numero}\n *Email: {request.user.email} \n Motivo: {motivo}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", adopcion.dueño.email]
                )
                send_mail(
                    "Solicitud de adopción - Información del perro",
                    f"Email del dueño: {adopcion.dueño.email} \n Nombre del perro: {adopcion.nombre} \n Fecha de nacimiento: {adopcion.fecha_nacimiento} \n Sexo: {adopcion.get_sexo_display()} \n Tamaño: {adopcion.get_tamaño_display()} \n Comentarios: {adopcion.comentarios}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", request.user.email]
                )
                return redirect("home")

        return render(request, "adopcion/contactar.html", {'formulario': form})
    else:
        form = FormularioDatosAdopcionNoUsuario()
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
                    f"{nombre} se quiere contactar para adoptar a {adopcion.nombre}.\n Esta es su información de contacto:\n *Numero: {numero}\n *Email: {email} \n Motivo: {motivo}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", adopcion.dueño.email]
                )
                send_mail(
                    "Solicitud de adopción - Información del perro",
                    f"Email del dueño: {adopcion.dueño.email} \n Nombre del perro: {adopcion.nombre} \n Fecha de nacimiento: {adopcion.fecha_nacimiento} \n Sexo: {adopcion.get_sexo_display()} \n Tamaño: {adopcion.get_tamaño_display()} \n Comentarios: {adopcion.comentarios}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", email]
                )
                return redirect("home")

        return render(request, "adopcion/contactar.html",{'formulario':form})
    

def no_hubo_cambios_post(posteo, formulario_adopcion):
    estado=posteo.nombre == formulario_adopcion.cleaned_data['nombre'] and posteo.fecha_nacimiento == formulario_adopcion.cleaned_data['fecha_nacimiento'] and posteo.sexo == formulario_adopcion.cleaned_data['sexo'] and posteo.tamaño == formulario_adopcion.cleaned_data['tamaño'] and posteo.comentarios == formulario_adopcion.cleaned_data['comentarios']
    print (estado) #sacar
    print ("posteorajjf")#sacar
    return estado


def formulario_posteo_inicial(posteo):
    formulario_adopcion = formulario_Adopcion(initial={
            'nombre': posteo.nombre,
            'fecha_nacimiento': posteo.fecha_nacimiento,
            'sexo': posteo.sexo,
            'tamaño': posteo.tamaño,
            'comentarios': posteo.comentarios
        })
    return formulario_adopcion


def guardar_datos(posteo, formulario_adopcion, dueño):
    posteo.dueño=dueño
    posteo.nombre = formulario_adopcion.cleaned_data['nombre']
    posteo.fecha_nacimiento = formulario_adopcion.cleaned_data['fecha_nacimiento']
    posteo.sexo = formulario_adopcion.cleaned_data['sexo']
    posteo.tamaño = formulario_adopcion.cleaned_data['tamaño']
    posteo.comentarios = formulario_adopcion.cleaned_data['comentarios']
    posteo.estado=Adopcion.Estado[0][1]
    posteo.save()
    

def editar_post_adopcion(request, adopcion_id):    
    posteo = Adopcion.objects.get(id=adopcion_id)
    
    if request.method=='POST':
        formulario_adopcion = formulario_Adopcion(data=request.POST)
        if formulario_adopcion.is_valid():
            if  no_hubo_cambios_post(posteo, formulario_adopcion):
                return render(request, 'adopcion/editar_post_adopcion.html', {'formulario_adopcion': formulario_posteo_inicial(posteo)})
            elif posteo.nombre != formulario_adopcion.cleaned_data['nombre']:
                if ya_esta_publicado(request.user, formulario_adopcion.data['nombre']):
                    #Agregar un mensaje error en el formulario html, cambiar el contexto mensaje por el valor error
                    error_ya_publicado="¡Ya tiene una mascota con ese nombre!"
                    return render (request, 'adopcion/editar_post_adopcion.html',{'formulario_adopcion':formulario_adopcion, "mensaje2":error_ya_publicado})
                else:
                    #guardar datos   
                    guardar_datos(posteo, formulario_adopcion, request.user) 
                    mensaje="Los cambios se han guardado correctamente."
                    return render(request, 'adopcion/editar_post_adopcion.html', {'formulario_adopcion': formulario_adopcion, "mensaje": mensaje})
            else:
               # guardar datos
                guardar_datos(posteo, formulario_adopcion, request.user) 
                mensaje="Los cambios se han guardado correctamente."
                return render(request, 'adopcion/editar_post_adopcion.html', {'formulario_adopcion': formulario_adopcion, "mensaje": mensaje})
    
    return render(request, 'adopcion/editar_post_adopcion.html', {'formulario_adopcion': formulario_posteo_inicial(posteo)})


#sacar si no se usa
"""
def editar_perro_adopcion(request, adopcion_id):    
    posteo = Adopcion.objects.get(id=adopcion_id)
    
    if request.method=='POST':
        formulario_adopcion = formulario_Adopcion(data=request.POST)
        if formulario_adopcion.is_valid():
            #Verifico que no tenga una mascota en adopción con el mismo nombre
            if ya_esta_publicado(request.user, formulario_adopcion.data['nombre']):
                #Agregar un mensaje error en el formulario html, cambiar el contexto mensaje por el valor error
                error_ya_publicado="¡Ya tiene publicada una mascota con ese nombre!"
                return render (request, 'adopcion/editar_post.html',{'formulario_adopcion':formulario_adopcion, "mensaje2":error_ya_publicado})
            else:
                posteo.dueño=request.user
                posteo.nombre = formulario_adopcion.cleaned_data['nombre']
                posteo.fecha_nacimiento = formulario_adopcion.cleaned_data['fecha_nacimiento']
                posteo.sexo = formulario_adopcion.cleaned_data['sexo']
                posteo.tamaño = formulario_adopcion.cleaned_data['tamaño']
                posteo.comentarios = formulario_adopcion.cleaned_data['comentarios']
                posteo.estado=Adopcion.Estado[0][1]
                posteo.save()
                mensaje="Los cambios se han guardado correctamente."
                return render(request, 'adopcion/editar_post.html', {'formulario_adopcion': formulario_adopcion, "mensaje": mensaje})

    else:
        formulario_adopcion = formulario_Adopcion(initial={
            'nombre': posteo.nombre,
            'fecha_nacimiento': posteo.fecha_nacimiento,
            'sexo': posteo.sexo,
            'tamaño': posteo.tamaño,
            'comentarios': posteo.comentarios
        })
        return render(request, 'adopcion/editar_post.html', {'formulario_adopcion': formulario_adopcion})
"""

def cerrar_post(request, adopcion_id): #mas adelante hacer que le pregunte al usuario si quiere o no realizar la operacion (paso intermedio)
    posteo = Adopcion.objects.get(id=adopcion_id)
    posteo.estado = Adopcion.Estado[1][1]
    posteo.save()   
    return redirect("adopcion")


def bajar_post(request, adopcion_id):
    print(adopcion_id)
    print(Adopcion.objects.get(id=adopcion_id))
    
    posteo = Adopcion.objects.get(id=adopcion_id)

    posteo.delete()
    return redirect("adopcion")

def ver_mis_perros_en_adopcion(request):
    publicaciones_del_usuario= Adopcion.objects.filter(dueño=request.user)
    return render(request, 'adopcion/ver_mis_perros_en_adopcion.html', {"publicaciones":publicaciones_del_usuario})
