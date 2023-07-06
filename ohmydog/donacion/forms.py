from django import forms
from .models import donacion
from datetime import date
from donacion.models import Tarjeta


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

class FormularioDonar(forms.Form):
    numero = forms.CharField(max_length=16)
    nombre_dueño= forms.CharField(max_length=50)
    monto = forms.IntegerField()
    codigo_seguridad = forms.CharField(max_length=3)
    mes_vencimiento = forms.CharField(max_length=2)
    año_vencimiento =forms.CharField(max_length=4)

   





