from django import forms
from .models import Proveedor
from perdidaBusqueda.models import Zona
from datetime import date



def numero_valido(value):
    guion=0
    for digit in value:
        if digit == '-':
            guion+=1
        if not digit.isdigit() and digit!='-':
            raise forms.ValidationError("Solo puede ingresar numeros y un -")
    if guion != 1:
        raise forms.ValidationError("Ingrese el codigo de area y luego el numero de telefono, separado por un guion")
        
def present_or_future_date(value):
    if value < date.today():
        raise forms.ValidationError("No puede ingresarse una fecha menor al dia de hoy")
    return value


class formulario_proveedor(forms.Form):
    nombre=forms.CharField(label="Nombre",max_length=15, required=True)
    apellido =forms.CharField(label="Apellido",max_length=15, required=True)
    email=forms.EmailField(label="Email")
    telefono=forms.CharField(label="Telefono",max_length=12, help_text="Caracteristica de zona - número de celular sin el 15", validators=[numero_valido])
    rol=forms.ChoiceField(label="Servicio prestado", choices=Proveedor.Roles)
    zona=forms.ModelChoiceField(label="Zona", queryset=Zona.objects.all())
    direccion=forms.CharField(required=False, help_text="Solo ingresar para los cuidadores")

class formulario_fecha(forms.Form):
    fecha_baja=forms.DateField(label='Fecha límite de baja', widget=forms.TextInput(     
        attrs={'type': 'date'} ), validators=[present_or_future_date])
    