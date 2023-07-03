from django.shortcuts import render,redirect
from .forms import formulario_proveedor, formulario_fecha
from .models import Proveedor

def contactoPaseadoresCuidadores (request):
    proveedores = Proveedor.objects.all()
    
    return render(request, "contactoPaseadoresCuidadores/contactoPaseadoresCuidadores.html",{'proveedores':proveedores})

def bajar_proveedor(request, proveedor_id):

    
    posteo = Proveedor.objects.get(id=proveedor_id)

    posteo.delete()
    return redirect('/contactoPaseadoresCuidadores/?elim')

def baja_temporaria(request, proveedor_id):
    fecha = formulario_fecha()

    if request.method == 'POST':
        fecha=formulario_fecha(data=request.POST)
        if fecha.is_valid():
            proveedor=Proveedor.objects.get(id=proveedor_id)
            proveedor.fecha_baja=fecha.cleaned_data['fecha_baja']
            proveedor.baja=True

            proveedor.save()

            return redirect('/contactoPaseadoresCuidadores/?temp')

    return render(request, 'contactoPaseadoresCuidadores/baja_temporal.html', {'form':fecha})


def alta_proveedor (request):
    formulario= formulario_proveedor()

    if request.method == 'POST':
        formulario= formulario_proveedor(data=request.POST)
        if formulario.is_valid():
            proveedor = Proveedor()

            proveedor.nombre=formulario.cleaned_data['nombre']
            proveedor.apellido=formulario.cleaned_data['apellido']
            proveedor.email=formulario.cleaned_data['email']
            proveedor.telefono=formulario.cleaned_data['telefono']
            proveedor.zona=formulario.cleaned_data['zona']
            proveedor.rol=formulario.cleaned_data['rol']
            if formulario.cleaned_data['direccion']:
                proveedor.direccion=formulario.cleaned_data['direccion']


            proveedor.save()

            return redirect('/contactoPaseadoresCuidadores/?valido')


    return render(request, 'contactoPaseadoresCuidadores/alta_proveedor.html', {'form':formulario})


