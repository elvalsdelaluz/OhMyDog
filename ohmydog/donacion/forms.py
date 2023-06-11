from django import forms
from .models import donacion
from datetime import date


def present_or_future_date(value):
    if value <= date.today():
        raise forms.ValidationError("La campaña no puede finalizar el mismo dia o dias antes del dia que comienza")
    return value

def no_solo_numeros(value):
    if value.isdigit():
        raise forms.ValidationError("El campo no puede contener solo números.")

####HACER VALIDACIONES POR FECHAS
class FormularioDonacion(forms.Form):
    motivo = forms.CharField(required=True, validators=[no_solo_numeros])
    descripcion = forms.CharField(required=True, validators=[no_solo_numeros])
    #imagen = forms.ImageField(required=True)
    finalizacion = forms.DateField(required=True, label='Fecha de finalizacion', widget=forms.TextInput(attrs={'type': 'date'}),
                            validators=[present_or_future_date])
