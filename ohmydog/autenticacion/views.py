from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from autenticacion.forms import RegistrationForm
import random
import string
from django.core.mail import send_mail

# Create your views here.
def autenticacion(request):
    return redirect ('home') #ESTO ME PA QUE NO VAAAAAAAAAAAAAAAAAAAAAAAAAA


def loguear(request):##arreglar
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
    return render(request, "autenticacion/login.html", {"form":form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')



def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def vista_registro(request, *args, **kwargs):
    user = request.user
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            edad = form.cleaned_data.get('edad')#mepa q no se usa
            password = generate_random_password()
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            destination = kwargs.get("next")
            send_mail("La contraseña para acceder al sitio ¡OhMyDog!", f"Hola {email}, gracias por registrarse en nuestro sitio. Su contraseña es: {password}", "OhMyDog@gmail.com", [email], fail_silently=False)
            if destination:
                return redirect(destination)
            return redirect("home")#cambiar redirect al formulario de registrar de un perro
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'autenticacion/register.html', context)