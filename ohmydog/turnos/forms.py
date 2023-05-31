from django import forms
from .models import Turno
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms.widgets import SelectDateWidget
from mascotas.models import Mascota
from datetime import date

def present_or_future_date(value):
    if value < date.today():
        raise forms.ValidationError("Por favor solicita un turno en una fecha valida")
    elif value == date.today():
        raise forms.ValidationError("Lo sentimos, los turnos son, cuanto menos, de un dia para el otro")
    elif value.weekday() == 6:
        raise forms.ValidationError("Lo sentimos, no trabajamos los domingos. Por favor elegi otro dia de la semana")
    return value

class formulario_turno(forms.Form):
    mascota = forms.ModelChoiceField(queryset=None)
    motivo = forms.ChoiceField(label='Motivo', choices=Turno.motivos)
    franja = forms.ChoiceField(label='Franja Horaria', choices=Turno.franja)
    fecha = forms.DateField(label='Fecha', widget=forms.TextInput(attrs={'type': 'date'}),
                            validators=[present_or_future_date])

    def __init__(self, user, *args, **kwargs):
        super(formulario_turno, self).__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascota.objects.filter(dueño=user)

    class Meta:
        model = Turno
        fields = [
            'mascota',
            'motivo',
            'franja',
            'fecha',
        ]



class Formulario_rechazado(forms.Form):
    motivo_rechazo = forms.CharField(widget=forms.Textarea, required=True)


class Formulario_concluido(forms.Form):
    observaciones = forms.CharField(widget=forms.Textarea, required=True, max_length=150)
    monto = forms.DecimalField(label='Monto en $', decimal_places=2,required=True)

class Formulario_aceptado(forms.Form):

    

    def __init__(self, franja, *args, **kwargs):
        super(Formulario_aceptado, self).__init__(*args, **kwargs)
        self.fields['hora'].choices = franja

    

    hora = forms.ChoiceField(label='Hora', choices=())
