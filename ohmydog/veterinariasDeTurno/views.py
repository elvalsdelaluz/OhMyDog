from django.shortcuts import render, redirect
from veterinariasDeTurno.models import VeterinariasDeTurno
from .forms import Formulario_archivo
import pandas as pd
import numpy as np

def borrar_archivo(request):
    open('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv', 'w').close()
    return redirect ('/veterinariasDeTurno/?valido')

def veterinariasDeTurno (request):

    formulario_archivo=Formulario_archivo()
    data_html=[]
    try:
        data =pd.read_csv('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv', delimiter=';')
        data = pd.DataFrame(data)
        
        data = data.replace(np.nan,'-')
        data_html=data.to_html(index=False, classes='table table-striped text-center', justify='center')
    
    except pd.errors.EmptyDataError:
        pass

    if request.method=='POST':
        file_form=Formulario_archivo(request.POST, request.FILES)

        if file_form.is_valid():
            csv_file=(request.FILES['archivo'])
            with open('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv', 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            return redirect('veterinariasDeTurno')
            """data = pd.read_csv(csv_file)
            df =pd.DataFrame(data)
            df.to_csv('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv', mode='w')"""

    return render(request, "veterinariasDeTurno/veterinariasDeTurno.html", {'form':formulario_archivo, 'data': data_html})
