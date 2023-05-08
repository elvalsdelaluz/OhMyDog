from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
def autenticacion(request):
    return redirect ('home') #ESTO ME PA QUE NO VAAAAAAAAAAAAAAAAAAAAAAAAAA


def loguear(request):
    if request.method == "POST": #quiere decir que el user clickeo el botón 
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contraseña=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:
                messages.error(request, "Hubo un error de autenticación, vuelva a intentarlo")
        else:
            messages.error(request, "Hubo un error de autenticación, vuelva a intentarlo")
    form=AuthenticationForm()
    return render(request, "login/login.html", {"form":form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')


