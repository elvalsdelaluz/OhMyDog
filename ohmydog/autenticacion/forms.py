from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate
from autenticacion.models import Cuenta


class RegistrationForm(UserChangeForm):
    email = forms.EmailField(max_length=60, help_text="Ingresa una dirección de correo válida")
    edad = forms.IntegerField(help_text="Ingresa tu edad")
    
    class Meta:
        model = Cuenta 
        fields = ('email','nombre', 'dni', 'numero', 'edad', 'password')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            cuenta = Cuenta.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'El mail {email} está en uso')

    def clean_edad(self):
        edad = self.cleaned_data['edad']
        if edad < 18:
            raise forms.ValidationError(f'Se debe ser mayor de 18 para registrarse')
        return edad
        
    