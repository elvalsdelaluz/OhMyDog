from django.shortcuts import render, redirect
from veterinariasDeTurno.models import VeterinariasDeTurno
from .forms import Formulario_archivo
import pandas as pd
import numpy as np
from django.contrib import messages


def borrar_archivo(request):
    open('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv', 'w').close()
    messages.add_message(request, messages.INFO, "El turnero se ha eliminado exitosamente")
    return redirect ('/veterinariasDeTurno/')

def convertidor(value):
    dict ={'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles',
           'Thursday':'Jueves','Friday':'Viernes','Saturday':'Sabado',
           'Sunday':'Domingo'}
    return dict[str(value)]
def traductor_mes(value):
    meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    return meses[value]

def mejorar_guardado(data):
        data = data.dropna(1, how='all')
        data = data.replace(np.nan,'-')
        x = 2
        for col in data.columns[2:]:
            data = data.rename(columns={col:'Direccion '+str(x)})
            x+=1
        data.to_csv('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv', index=False)
    

def veterinariasDeTurno (request):
    formulario_archivo=Formulario_archivo()
    data1_html=[]
    data2_html=[]
    mes=[]
    try:
        data =pd.read_csv('../ohmydog/veterinariasDeTurno/file/vetTurnos.csv')
        data = pd.DataFrame(data)
        data["Dia"]  = pd.to_datetime(data["Dia"], format='%Y/%m/%d')
        mes = traductor_mes(data.iloc[1]["Dia"].month-1) + ' ' + data.iloc[1]["Dia"].strftime("%Y")
        data["Dia"] =  data['Dia'].apply(lambda x : convertidor(x.day_name())) + ' ' + data["Dia"].dt.strftime("%d")
        data1=data.head(int(len(data)/2))
        data2=data.tail(-int(len(data)/2))
        data1_html=data1.to_html(index=False, classes='table table-striped text-center', justify='center')
        data2_html=data2.to_html(index=False, classes='table table-striped text-center', justify='center')

    
    except pd.errors.EmptyDataError:
        pass

    if request.method=='POST':
        file_form=Formulario_archivo(request.POST, request.FILES)

        if file_form.is_valid():
            try:
                data =pd.read_csv(request.FILES['archivo'], encoding='unicode_escape',delimiter=';')
            except UnicodeDecodeError:
                messages.add_message(request, messages.ERROR, "Lo sentimos. Hubo un error de decodificacion del archivo. Por favor revise los caracteres especiales y envielo nuevamente")
                return redirect ('/veterinariasDeTurno/')
            data = pd.DataFrame(data)
            if data.columns[0] !='Dia' or data.columns[1] !='Direccion':
                messages.add_message(request, messages.ERROR, "La primera columna debe llamarse 'Dia' e incluir las fechas del mes. y la segunda 'Direccion'")
                return redirect ('/veterinariasDeTurno/')
            try:
                data = data.dropna(0, how='all')
                data["Dia"]  = pd.to_datetime(data["Dia"], format='%d/%m/%Y')
            except ValueError:
                messages.add_message(request, messages.ERROR, "Por favor, chequea que todos los datos de la columna 'Dia' sean fechas validas con formato DD/MM/AAAA")
                return redirect ('/veterinariasDeTurno/')
            mejorar_guardado(data)

            return redirect('veterinariasDeTurno')
        else:
            messages.add_message(request, messages.ERROR, "Solo puede subir archivos en formato CSV")
            return redirect ('/veterinariasDeTurno/')



    return render(request, "veterinariasDeTurno/veterinariasDeTurno.html", {'form':formulario_archivo, 'data': data1_html, 'data1':data2_html, 'mes':mes})
