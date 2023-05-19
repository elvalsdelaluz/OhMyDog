from django import forms
from .models import Adopcion
from django.contrib.auth.models import User
from datetime import date

def present_or_future_date(value):
    if value > date.today():
        raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro")
    return value



class formulario_Adopcion(forms.Form):
    nombre=forms.CharField(label='Nombre', required=True)
    fecha_nacimiento=forms.DateField(label='Fecha nacimiento', widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    sexo=forms.ChoiceField(label='Sexo', choices=Adopcion.Sexo)
    tamaño=forms.ChoiceField(label='Tamaño', choices=Adopcion.Tamaño)
    comentarios=forms.CharField(label='Comentarios', widget=forms.Textarea)



class FormularioDatosAdopcionLogueado(forms.Form):  
    motivo=forms.CharField(label='motivo', widget=forms.Textarea, required=True)

class FormularioDatosAdopcionNoUsuario(FormularioDatosAdopcionLogueado):  
    nombre=forms.CharField(label='nombre', required=True)
    email = forms.EmailField(max_length=60, required=True)
    numero=forms.CharField(label='numero', required=True)