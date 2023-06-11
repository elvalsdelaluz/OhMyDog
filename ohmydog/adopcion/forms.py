from django import forms
from .models import Adopcion
from django.contrib.auth.models import User
from datetime import date
import re
def present_or_future_date(value):
    if value > date.today():
        raise forms.ValidationError("No pueden publicarse perros aun no nacidos")
    return value


def no_solo_numeros(value):
    if value.isdigit():
        raise forms.ValidationError("El campo no puede contener solo números.")

def no_contiene_numeros(value):
    if re.search(r'\d', value):
        raise forms.ValidationError("El campo no puede contener números.")

class formulario_Adopcion(forms.Form):
    nombre=forms.CharField(label='Nombre', required=True,validators=[no_contiene_numeros])
    fecha_nacimiento=forms.DateField(label='Fecha nacimiento', widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    sexo=forms.ChoiceField(label='Sexo', choices=Adopcion.Sexo)
    tamaño=forms.ChoiceField(label='Tamaño', choices=Adopcion.Tamaño)
    comentarios=forms.CharField(label='Comentarios', widget=forms.Textarea,validators=[no_solo_numeros])



class FormularioDatosAdopcionLogueado(forms.Form):  
    motivo=forms.CharField(label='motivo', widget=forms.Textarea(attrs={'resize': 'none'}), required=True,validators=[no_solo_numeros])

class FormularioDatosAdopcionNoUsuario(FormularioDatosAdopcionLogueado):  
    nombre=forms.CharField(label='nombre', required=True,validators=[no_contiene_numeros])
    email = forms.EmailField(max_length=60, label='email', required=True)
    numero=forms.CharField(max_length=10, label='numero', required=True)

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if len(numero) < 10:
            raise forms.ValidationError('Número de teléfono inválido')
        if not numero.isdigit():
            raise forms.ValidationError('Error en el formato del número de telefono. Ingrese solo el número')
        return numero