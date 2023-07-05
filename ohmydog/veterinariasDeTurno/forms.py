from django import forms
from django.core.validators import FileExtensionValidator



class Formulario_archivo(forms.Form):
    archivo=forms.FileField(label="Archivo", help_text="Por favor, ingrese el archivo en formato .csv",
                            validators=[FileExtensionValidator(['csv'], message="Solo puede subir archivos en formato .CSV" ) ],)
    