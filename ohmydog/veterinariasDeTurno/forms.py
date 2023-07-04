from django import forms


class Formulario_archivo(forms.Form):
    archivo=forms.FileField(label="Archivo", help_text="Por favor, ingrese el archivo en formato csv")