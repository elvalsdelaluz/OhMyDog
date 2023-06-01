from django import forms
from .models import donacion
from datetime import date



####HACER VALIDACIONES POR FECHAS
class FormularioDonacion(forms.Form):
    motivo = forms.CharField(required=True)
    descripcion = forms.CharField(required=True)
    #imagen = forms.ImageField(required=True)
    finalizacion = forms.DateField(required=True, label='fecha', widget=forms.TextInput(attrs={'type': 'date'}))