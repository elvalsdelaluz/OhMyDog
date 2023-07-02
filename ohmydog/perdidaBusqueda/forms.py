from django import forms
from .models import PerroPerdido
from mascotas.models import Raza, Mascota
from django.contrib.auth.models import User
from datetime import date
import re
def present_or_future_date(value):
    if value > date.today():
        raise forms.ValidationError("No pueden publicarse perros que se pierden en el futuro")
    return value


def no_solo_numeros(value):
    if value.isdigit():
        raise forms.ValidationError("El campo no puede contener solo números.")

def no_contiene_numeros(value):
    print(value)
    if re.search(r'\d', value):
        raise forms.ValidationError("El campo no puede contener números.")

class PerroPerdidoForm(forms.Form):
    Estado=(
        ('0','Extraviado'),
        ('1','Encontrado'),
    )
    estado=forms.ChoiceField(label="Estado", choices=Estado)
    nombre=forms.CharField(label='Nombre', required=False)
    foto=forms.ImageField(label="Foto", required=False)
    fecha_perdido=forms.DateField(label='Fecha perdido o encontrado', widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    fecha_nacimiento=forms.DateField(label='Fecha nacimiento', required=False, widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    tamaño=forms.ChoiceField(label='Tamaño', choices=PerroPerdido.Tamaño)
    sexo=forms.ChoiceField(label='Sexo', choices=PerroPerdido.Sexo)
    raza=forms.ChoiceField(label="Raza", required=False, choices=Mascota.razas_choices)
    zona=forms.CharField(label='Zona', required=True) #entiendo que esto es una direccion tipo 7 y 50 por eso creo que la validación de números no es necesaria

    comentario=forms.CharField(label='Comentarios', widget=forms.Textarea,validators=[no_solo_numeros])

