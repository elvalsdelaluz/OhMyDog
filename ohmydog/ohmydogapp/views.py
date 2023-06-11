from django.shortcuts import render
from mascotas.models import Mascota
from mascotas.views import alta_mascota
from django.shortcuts import redirect

def home (request):
    usuario_autenticado = request.user
    if usuario_autenticado.is_authenticated and not usuario_autenticado.is_staff:
        #pregunto si tiene perros
        tiene_perros = Mascota.objects.filter(dueño=usuario_autenticado).exists()
        if not tiene_perros:
             return redirect('alta_mascota/?valido2')
        else:
             return render(request, "ohmydogapp/home.html")  
    else:
        return render(request, "ohmydogapp/home.html")

