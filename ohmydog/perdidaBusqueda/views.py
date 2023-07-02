from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PerroPerdido
from mascotas.models import Mascota
from .forms import PerroPerdidoForm

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


def ya_esta_publicado(user, nombre_mascota):  
    """Si el usuario ya tiene una publicación con nombre, fecha y sexo 
       la función devuelve true
    """ 
    existe_publicacion=False
    publicaciones_del_usuario= PerroPerdido.objects.filter(dueño=user)

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


def publicar_perro_perdido(request):
    formulario_perro_perdido = PerroPerdidoForm()

    if request.method=='POST':
        formulario_perro_perdido=PerroPerdidoForm(request.POST, request.FILES)
       
        if formulario_perro_perdido.is_valid():
            if ya_esta_publicado(request.user, formulario_perro_perdido.cleaned_data['nombre']):
                #Agregar un mensaje error en el formulario html, cambiar el contexto mensaje por el valor error
                error_ya_publicado="¡Ya tiene publicada una mascota perdida con ese nombre!"
                return render (request, 'perdidaBusqueda/publicar_perro_perdido.html', {'formulario_perro_perdido':formulario_perro_perdido, "mensaje2":error_ya_publicado})
            else:
                #Queda cambiarle el nombre a la foto... 
                publicacion_perro_perdido=PerroPerdido()
                publicacion_perro_perdido.dueño=request.user
                publicacion_perro_perdido.nombre=formulario_perro_perdido.cleaned_data['nombre']
                
                if request.FILES:
                    foto_file=request.FILES['foto']
                else:
                    foto_file=None


                publicacion_perro_perdido.fecha_perdido=formulario_perro_perdido.cleaned_data['fecha_perdido']
                publicacion_perro_perdido.fecha_nacimiento=formulario_perro_perdido.cleaned_data['fecha_nacimiento']
                
                publicacion_perro_perdido.tamaño=formulario_perro_perdido.cleaned_data['tamaño']
                publicacion_perro_perdido.sexo=formulario_perro_perdido.cleaned_data['sexo']
                
                 
                publicacion_perro_perdido.raza=formulario_perro_perdido.cleaned_data['raza']
                publicacion_perro_perdido.zona=formulario_perro_perdido.cleaned_data['zona']
             
                publicacion_perro_perdido.estado=formulario_perro_perdido.cleaned_data['estado']
                publicacion_perro_perdido.comentario=formulario_perro_perdido.cleaned_data['comentario']

                publicacion_perro_perdido.save()

                publicacion_perro_perdido.foto=foto_file
                publicacion_perro_perdido.save()

                formulario_perro_perdido=PerroPerdidoForm()

                return render (request, 'perdidaBusqueda/publicar_perro_perdido.html',{'formulario_perro_perdido':formulario_perro_perdido, "mensaje":"ok"})

    return render(request, "perdidaBusqueda/publicar_perro_perdido.html", {"formulario_perro_perdido":formulario_perro_perdido})


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

