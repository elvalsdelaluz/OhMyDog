from django import forms
from .models import Adopcion

class formulario_Adopcion(forms.Form):
    nombre=forms.CharField(label='Nombre', required=True)
    edad=forms.IntegerField(label='Edad', required=True)
    sexo=forms.ChoiceField(label='Sexo', choices=Adopcion.Sexo)
    tamaño=forms.ChoiceField(label='Tamaño', choices=Adopcion.Tamaño)
    estado=forms.ChoiceField(label='Estado', choices=Adopcion.Estado, initial='0')
    comentarios=forms.CharField(label='Comentarios', widget=forms.Textarea)