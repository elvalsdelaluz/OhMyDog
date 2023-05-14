from django.shortcuts import render, redirect
from adopcion.models import Adopcion
from .forms import formulario_Adopcion, FormularioDatosAdopcionLogueado, FormularioDatosAdopcionNoUsuario
from django.core.mail import send_mail

def adopcion (request):
    return render(request, "adopcion/adopcion.html", {"adopciones":Adopcion.objects.all()})


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
            nueva_adopcion.edad=formulario_adopcion.cleaned_data['edad']
            nueva_adopcion.tamaño=formulario_adopcion.cleaned_data['tamaño']
            nueva_adopcion.estado=formulario_adopcion.cleaned_data['estado']
            nueva_adopcion.comentarios=formulario_adopcion.cleaned_data['comentarios']

            nueva_adopcion.save()

            formulario_adopcion=formulario_Adopcion()

            return render (request, 'adopcion/adopcion/solicitud.html',{'formulario':formulario_adopcion, "mensaje":"ok"})
        
    return render(request, 'adopcion/adopcion/solicitud.html', {'formulario':formulario_adopcion})


'''
#no terminado. EN PROCESOOOO
def datos_adopcion(request, adopcion_id):
    user = request.user
    if user.is_authenticated:
        if request.method =='POST':
            form = FormularioDatosAdopcionLogueado(request.POST)
            motivo = form.cleaned_data('motivo')
            adopcion = Adopcion.objects.filter(id=adopcion_id)
            send_mail("Solicitud de adopción", f"{request.user.email} se quiere contactar para adoptar el perro que publicaste.\n{motivo}", "OhMyDog@gmail.com", ["matolu.enterprise@gmail.com", request.user.email, adopcion.dueño.email])
            return redirect("/home/?valido")
'''
    