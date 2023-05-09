from django.shortcuts import render, redirect
from adopcion.models import Adopcion
from .forms import formulario_Adopcion

def adopcion (request):
    return render(request, "adopcion/adopcion.html", {"adopciones":Adopcion.objects.all()})


def publicacion(request):

    formulario_adopcion=formulario_Adopcion()

    if request.method=='POST':
        formulario_adopcion=formulario_Adopcion(data=request.POST)
        if formulario_adopcion.is_valid():
            #Aca hay que hacerlo andar
            nueva_adopcion=Adopcion()
            nueva_adopcion.nombre=formulario_adopcion.cleaned_data['nombre']
            nueva_adopcion.sexo=formulario_adopcion.cleaned_data['sexo']
            nueva_adopcion.edad=formulario_adopcion.cleaned_data['edad']
            nueva_adopcion.tamaño=formulario_adopcion.cleaned_data['tamaño']
            nueva_adopcion.estado=formulario_adopcion.cleaned_data['estado']
            nueva_adopcion.comentarios=formulario_adopcion.cleaned_data['comentarios']

            nueva_adopcion.save()

            #return redirect ('adopcion/solicitud/?valido')
        
    return render(request, 'adopcion/adopcion/solicitud.html', {'formulario':formulario_adopcion})
