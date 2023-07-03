from django.shortcuts import render,redirect
from .forms import formulario_proveedor, formulario_fecha, Filtro
from .models import Proveedor
from datetime import date



def contactoPaseadoresCuidadores (request):
    proveedores = Proveedor.objects.all()
    filtro= Filtro()

    if proveedores.filter(baja=True).exists():
        for prov in proveedores.filter(baja=True):
            if prov.fecha_baja<=date.today():
                prov.baja=False
                prov.fecha_baja=None
                prov.save()
    if request.method == 'POST':
        filtro=Filtro(data=request.POST)
        if filtro.is_valid():
            if filtro.cleaned_data['rol']!='2':
                proveedores=proveedores.filter(rol=filtro.cleaned_data['rol']).all()
            if filtro.cleaned_data['zona']:
                proveedores=proveedores.filter(zona=filtro.cleaned_data['zona']).all()
            

    
    return render(request, "contactoPaseadoresCuidadores/contactoPaseadoresCuidadores.html",{'proveedores':proveedores, 'filtro':filtro})

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


