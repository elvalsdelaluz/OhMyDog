from django import forms
from .models import PerroPerdido, Zona
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
    perro = forms.ModelChoiceField(
        queryset=Mascota.objects.all(),
        required=False,
        empty_label='Perro no registrado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nombre=forms.CharField(label='Nombre', required=False)
    fecha_nacimiento=forms.DateField(label='Fecha nacimiento', required=False, widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    sexo=forms.ChoiceField(label='Sexo', choices=PerroPerdido.Sexo)
    raza=forms.ChoiceField(label="Raza", required=False, choices=Mascota.razas_choices)
    estado=forms.ChoiceField(label="Estado", choices=Estado)
    foto=forms.ImageField(label="Foto", required=False)
    tamaño=forms.ChoiceField(label='Tamaño', choices=PerroPerdido.Tamaño)
    fecha_perdido=forms.DateField(label='Fecha perdido o encontrado', widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    zona=forms.ModelChoiceField(label='Zona', required=True, queryset=Zona.objects.all()) #entiendo que esto es una direccion tipo 7 y 50 por eso creo que la validación de números no es necesaria

    def __init__(self, mis_perros=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perro'].queryset = mis_perros


class ContartarsePerroPerdidoLogueadoForm(forms.Form):  
    mensaje=forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'resize': 'none'}), required=False)

class ContartarsePerroPerdidoNoLogueadoForm(ContartarsePerroPerdidoLogueadoForm):  
    nombre=forms.CharField(label='Nombre', required=True,validators=[no_contiene_numeros])
    numero=forms.CharField(max_length=10, label='Numero telefono', required=True)
    email = forms.EmailField(max_length=60, label='Email', required=True)

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if len(numero) < 10:
            raise forms.ValidationError('Número de teléfono inválido')
        if not numero.isdigit():
            raise forms.ValidationError('Error en el formato del número de telefono. Ingrese solo el número')
        return numero
    

