from django import forms
from .models import Adopcion
from django.contrib.auth.models import User


class formulario_Adopcion(forms.Form):
    nombre=forms.CharField(label='Nombre', required=True)
    edad=forms.IntegerField(label='Edad', required=True)
    sexo=forms.ChoiceField(label='Sexo', choices=Adopcion.Sexo)
    tamaño=forms.ChoiceField(label='Tamaño', choices=Adopcion.Tamaño)
    estado=forms.ChoiceField(label='Estado', choices=Adopcion.Estado, initial='0')
    comentarios=forms.CharField(label='Comentarios', widget=forms.Textarea)



class FormularioDatosAdopcionLogueado(forms.Form):  
    motivo=forms.CharField(label='motivo', widget=forms.Textarea, required=True)

class FormularioDatosAdopcionNoUsuario(FormularioDatosAdopcionLogueado):  
    nombre=forms.CharField(label='nombre', required=True)
    email = forms.EmailField(max_length=60, required=True)
    numero=forms.CharField(label='numero', required=True)