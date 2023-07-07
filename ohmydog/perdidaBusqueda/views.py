from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PerroPerdido
from mascotas.models import Mascota
from .forms import PerroPerdidoForm, ContartarsePerroPerdidoNoLogueadoForm, ContartarsePerroPerdidoLogueadoForm, PerroForm
from django.core.mail import send_mail


def perdidaBusqueda (request):
    return render(request, "perdidaBusqueda/perdidaBusqueda.html")

def mostrar_perros_perdidos(request):
    ##########################################################
    ###################BLOQUEO OPCION#########################
    usuario_autenticado = request.user
    if usuario_autenticado.is_authenticated and not usuario_autenticado.is_staff:
        #pregunto si tiene perros  
        tiene_perros = Mascota.objects.filter(dueño=usuario_autenticado).exists()
        if not tiene_perros:
            return redirect('alta_mascota')
    ##########################################################

    '''Se muestra la plantilla adopcion.html la cual muestra las publicaciones de perros en adopción'''
    perdidos = PerroPerdido.objects.all()
    return render(request, "perdidaBusqueda/mostrar_perros_perdidos.html", {"perros_perdidos":perdidos})



from django.http import JsonResponse
    
def perro(request, perro_id):
    print("Se selecciono un perro")
    try:
        perro = Mascota.objects.get(id=perro_id)
        data = {
            'nombre': perro.nombre,
            'fecha_nacimiento': perro.fecha_nacimiento,
            'sexo': perro.sexo,
            'raza': perro.raza,
            'dueño': perro.dueño.id,
        }
        return JsonResponse(data)
    except Mascota.DoesNotExist:
        return JsonResponse({'error': 'Perro not found'}, status=404)


def publicar_perro_perdido(request):
    # Obtener el objeto deseado para sobrescribir el campo ModelChoiceField
    mis_perros = Mascota.objects.filter(dueño=request.user)
    # Crear una instancia del formulario
    formulario_perro_perdido = PerroPerdidoForm(mis_perros=mis_perros)

    if request.method=='POST':
        formulario_perro_perdido=PerroPerdidoForm(mis_perros, request.POST, request.FILES)
       
        if formulario_perro_perdido.is_valid():
            #Queda cambiarle el nombre a la foto... 
            publicacion_perro_perdido=PerroPerdido()
            publicacion_perro_perdido.dueño=request.user
            publicacion_perro_perdido.nombre=formulario_perro_perdido.cleaned_data['nombre']
                
            if request.FILES:
                foto_file=request.FILES['foto']
            else:
               foto_file=None


            publicacion_perro_perdido.fecha_perdido=formulario_perro_perdido.cleaned_data['fecha_perdido']

            if not formulario_perro_perdido.cleaned_data['fecha_nacimiento']:
                publicacion_perro_perdido.fecha_nacimiento=None
            else:
                publicacion_perro_perdido.fecha_nacimiento=formulario_perro_perdido.cleaned_data['fecha_nacimiento']
                    
            publicacion_perro_perdido.tamaño=formulario_perro_perdido.cleaned_data['tamaño']
            publicacion_perro_perdido.sexo=formulario_perro_perdido.cleaned_data['sexo']
                
                 
            publicacion_perro_perdido.raza=formulario_perro_perdido.cleaned_data['raza']
            publicacion_perro_perdido.zona=formulario_perro_perdido.cleaned_data['zona']
             
            publicacion_perro_perdido.estado=formulario_perro_perdido.cleaned_data['estado']
            #publicacion_perro_perdido.comentario=formulario_perro_perdido.cleaned_data['comentario']

            publicacion_perro_perdido.save()

            publicacion_perro_perdido.foto=foto_file
            publicacion_perro_perdido.save()

            formulario_perro_perdido=PerroPerdidoForm(mis_perros=mis_perros)

            return render (request, 'perdidaBusqueda/publicar_perro_perdido.html',{'form':formulario_perro_perdido, "mensaje":"ok"})

    return render(request, "perdidaBusqueda/publicar_perro_perdido.html", {"form":formulario_perro_perdido})


def cambiar_a_localizado(request, perdido_id): #mas adelante hacer que le pregunte al usuario si quiere o no realizar la operacion (paso intermedio)
    posteo = PerroPerdido.objects.get(id=perdido_id)
    posteo.estado = PerroPerdido.Estado[2][1]
    posteo.save()   
    messages.success(request, '¡Se ha cambiado el estado de la publicación!')
    return redirect('mostrar_perros_perdidos')


def eliminar_publicacion(request, perdido_id):
    print(perdido_id)
    print(PerroPerdido.objects.get(id=perdido_id))
    
    posteo = PerroPerdido.objects.get(id=perdido_id)

    posteo.delete()
    messages.success(request, '¡La publicacion se ha eliminado correctamente!')
    return redirect('mostrar_perros_perdidos')
    #return render(request, "perdidaBusqueda/mostrar_perros_perdidos.html", {"valido":True})

def comunicarse_por_perro_perdido(request, perdido_id):
    user = request.user
    
    if user.is_authenticated:
        form = ContartarsePerroPerdidoLogueadoForm()
        if request.method == 'POST':
            form = ContartarsePerroPerdidoLogueadoForm(request.POST)
            if form.is_valid():
                mensaje= form.cleaned_data['mensaje']
                perro_perdido = PerroPerdido.objects.get(id=perdido_id)
                send_mail(
                    "Hola.",
                    f"{request.user.nombre} se quiere contactarse con usted por {perro_perdido.nombre}.\n Esta es su información de contacto:\n *Numero: {request.user.numero}\n *Email: {request.user.email} \n Mensaje: {mensaje}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", perro_perdido.dueño.email]
                )
                messages.success(request, '¡Su mensaje ha sido enviado!')    
                return redirect("mostrar_perros_perdidos")

        return render(request, "perdidaBusqueda/comunicarse_por_perro_perdido.html", {'formulario': form, 'info_autocompletada': user})
    else:
        form = ContartarsePerroPerdidoNoLogueadoForm()
        if request.method == 'POST':
            form = ContartarsePerroPerdidoNoLogueadoForm(request.POST)
            if form.is_valid():
                nombre= form.cleaned_data['nombre']
                numero_telefono= form.cleaned_data['numero']
                email= form.cleaned_data['email']
                mensaje=form.cleaned_data['mensaje']
                perro_perdido = PerroPerdido.objects.get(id=perdido_id)
                send_mail(
                    "Hola.",
                    f"{nombre} se quiere contactarse con usted por {perro_perdido.nombre}.\n Esta es su información de contacto:\n *Numero: {numero_telefono}\n *Email: {email} \n Mensaje: {mensaje}",
                    "ohmydog.veterinariacanina@gmail.com",
                    ["ohmydog.veterinariacanina@gmail.com", perro_perdido.dueño.email]
                )
                messages.success(request, '¡Su mensaje ha sido enviado!')    
                return redirect("mostrar_perros_perdidos")

               
        return render(request, "perdidaBusqueda/comunicarse_por_perro_perdido.html", {'formulario': form})
