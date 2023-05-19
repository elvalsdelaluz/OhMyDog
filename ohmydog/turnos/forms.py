from django import forms
from .models import Turno
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms.widgets import SelectDateWidget
from mascotas.models import Mascota
from crum import get_current_user





class formulario_turno(forms.Form,):

    
    current = get_current_user

  
    mascota=forms.ModelChoiceField(queryset=(Mascota.objects.all()))
    motivo=forms.ChoiceField(label='Motivo', choices=Turno.motivos)
    franja=forms.ChoiceField(label='Franja Horaria', choices=Turno.franja)
    fecha=forms.DateField(label='Fecha', widget=forms.TextInput(     
        attrs={'type': 'date'} ))
    

    class Meta:
        model=Turno
        fields = [
            'mascota',
            'motivo',
            'franja',
            'fecha',
        ]


