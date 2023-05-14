from django import forms
from .models import Turno
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms.widgets import SelectDateWidget                                    



class formulario_turno(forms.Form):
    mascota=forms.CharField(label='Mascota', required=True)
    motivo=forms.ChoiceField(label='Motivo', choices=Turno.motivos)
    franja=forms.ChoiceField(label='Franja Horaria', choices=Turno.franja)
    fecha=forms.DateField(label='Fecha',widget=SelectDateWidget)
    

    class Meta:
        model=Turno

    def __init__(self, *args, **kwargs):
        super(formulario_turno, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget = SelectDateWidget()