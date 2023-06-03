from django import forms
from .models import Mascota, EntradaLibretaSanitaria


class MascotaForm(forms.Form):
    #Si el usuario que inicio sesión es staff se va a mostrar el campo
    #email dueño (definido en el html) a parte de los siguientes campos:
    nombre=forms.CharField(label='Nombre', required=True)
    raza=forms.ChoiceField(label='Raza', choices=Mascota.razas_choices)
    sexo=forms.ChoiceField(label='Sexo', choices=Mascota.sexo_choices)
    fecha_nacimiento=forms.DateField(label='Fecha nacimiento', widget=forms.TextInput(     
        attrs={'type': 'date'} ))
    observaciones=forms.CharField(label='Observaciones', widget=forms.Textarea, required=False) 


class EntradaLibretaSanitariaForm(forms.Form):
    peso=forms.DecimalField()
    cantidad_desparacitario=forms.DecimalField(required=False) #En caso de ser vacuna A o B no se va a completar