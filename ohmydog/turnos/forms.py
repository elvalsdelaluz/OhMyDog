from django import forms
from .models import Turno
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms.widgets import SelectDateWidget
from mascotas.models import Mascota
from django import forms
from .models import Turno
from mascotas.models import Mascota

class formulario_turno(forms.Form):
    mascota = forms.ModelChoiceField(queryset=None)
    motivo = forms.ChoiceField(label='Motivo', choices=Turno.motivos)
    franja = forms.ChoiceField(label='Franja Horaria', choices=Turno.franja)
    fecha = forms.DateField(label='Fecha', widget=forms.TextInput(attrs={'type': 'date'}))

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