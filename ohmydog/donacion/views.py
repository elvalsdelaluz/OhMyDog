from django.shortcuts import render

def donacion (request):
    return render(request, "donacion/donacion.html")