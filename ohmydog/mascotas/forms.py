from django import forms
from .models import Mascota

class MascotaForm(forms.Form):
    nombre=forms.CharField(label='Nombre', required=True)
    raza=forms.ChoiceField(label='Raza', choices=Mascota.razas_choices)
    sexo=forms.ChoiceField(label='Sexo', choices=Mascota.sexo_choices)
    fecha_nacimiento=forms.DateField(label='Fecha nacimiento', widget=forms.SelectDateWidget)
    observaciones=forms.CharField(label='Observaciones', widget=forms.Textarea)