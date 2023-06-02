from django import forms
from .models import donacion
from datetime import date


def present_or_future_date(value):
    if value <= date.today():
        raise forms.ValidationError("La campaña no puede finalizar el mismo dia o dias antes del dia que comienza")
    return value

####HACER VALIDACIONES POR FECHAS
class FormularioDonacion(forms.Form):
    motivo = forms.CharField(required=True)
    descripcion = forms.CharField(required=True)
    #imagen = forms.ImageField(required=True)
    finalizacion = forms.DateField(required=True, label='Fecha', widget=forms.TextInput(attrs={'type': 'date'}),
                            validators=[present_or_future_date])