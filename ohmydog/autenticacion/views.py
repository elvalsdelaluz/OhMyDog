from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from autenticacion.forms import RegistrationForm, FormularioCambiarContraseña
import random
import string
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.urls import reverse
from mascotas.models import Mascota
# Create your views here.


def tiene_mascotas(usuario_dueño):
    tiene=False
    mascotas = Mascota.objects.filter(dueño=usuario_dueño)
    if mascotas.exists():
        tiene = True
    return tiene

def loguear(request):
    if request.method == "POST": #quiere decir que el user clickeo el botón iniciar sesión
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contraseña=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                if tiene_mascotas(usuario):
                    #No tiene mascotas registradas
                    return redirect('home')
                elif usuario.is_staff:
                    return redirect('turnos_pendientes')
                else:
                    return redirect('alta_mascota')
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
            nombre = form.cleaned_data.get('nombre')#mepa q no se usa
            password = generate_random_password()
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            destination = kwargs.get("next")
            send_mail("La contraseña para acceder al sitio ¡OhMyDog!", f"Hola {nombre}, gracias por registrarse en nuestro sitio. Su contraseña es: {password}", "ohmydog.veterinariacanina@gmail.com", [email], fail_silently=False)
            if destination: #ver q mierda es esto
                return redirect(destination)
            return redirect(reverse('alta_mascota') + f'?email={email}')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'autenticacion/register.html', context)


@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = FormularioCambiarContraseña(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FormularioCambiarContraseña(request.user)
    return render(request, 'cuenta/cambiar_contraseña.html', {'form': form})