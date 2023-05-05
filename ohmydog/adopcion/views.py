from django.shortcuts import render

def adopcion (request):
    return render(request, "adopcion/adopcion.html")
