from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from pullTest.form import RegistroTest
from .models import PullTest
from django.contrib.auth import logout
import io
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
from datetime import datetime


# Create your views here.
def index(request):
    user=request.user
    if user is not None and user.is_authenticated: 
        template = loader.get_template('index.html')
        registros=PullTest.objects.all().values().order_by('-id')
        context={ 'title':'Titulo de paguina','registros':registros,'user':user }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')
def test(request):
    user=request.user
    if user is not None and user.is_authenticated: 
        if request.method == 'POST':
            form = RegistroTest(request.POST)
            if form.is_valid():
                term=form.cleaned_data['cont'].upper()
                form.instance.cont=term
                form.instance.val=user
                if((form.cleaned_data['calibre'] == '6' and (form.cleaned_data['presion']>=225) and (term!="MT1-54" or term!="MT1-54"  )) or
                  (form.cleaned_data['calibre'] == '10' and (form.cleaned_data['presion']>=80) and (form.cleaned_data['presion']<=161.12) and (term!="MT1-54" or term!="MT1-4"  )) or 
                  (form.cleaned_data['calibre'] == '12' and (form.cleaned_data['presion']>=70) and (form.cleaned_data['presion']<=148.95) and (term!="MT1-54" or term!="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '14' and (form.cleaned_data['presion']>=50) and (form.cleaned_data['presion']<=93.32) and (term!="MT1-54" or term!="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '16' and (form.cleaned_data['presion']>=30) and (form.cleaned_data['presion']<=83.13) and (term!="MT1-54" or term!="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '18' and (form.cleaned_data['presion']>=20) and (form.cleaned_data['presion']<=66.4) and (term!="MT1-54" or term!="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '20' and (form.cleaned_data['presion']>=13) and (form.cleaned_data['presion']<=46.39) and (term!="MT1-54" or term!="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '22' and (form.cleaned_data['presion']>=8) and (form.cleaned_data['presion']<=44.95) and (term!="MT1-54" or term!="MT1-4"  )) ):
                    form.instance.tipo="OK"
                    form.save()
                    return redirect('/pull')
                elif( (form.cleaned_data['calibre'] == '14' and (form.cleaned_data['presion']>=21) and (term=="MT1-54" or term=="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '16' and (form.cleaned_data['presion']>=19.8) and (term=="MT1-54" or term=="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '18' and (form.cleaned_data['presion']>=19.8) and (term=="MT1-54" or term=="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '20' and (form.cleaned_data['presion']>=13.3) and (term=="MT1-54" or term=="MT1-4"  )) or
                  (form.cleaned_data['calibre'] == '22' and (form.cleaned_data['presion']>=8.78) and (term=="MT1-54" or term=="MT1-4"  )) ):
                    form.instance.tipo="OK Minifit"
                    form.save()
                    return redirect('/pull')
                else:
                    form.instance.tipo="Mala"
                    form.save()
                    return redirect('/pull/malas')     
                
                    
        else:
            form = RegistroTest()
            registros = PullTest.objects.all().order_by('-id')
        return render(request, 'test-pull.html', {'form': form,'registros':registros})  
    else:
        return redirect('/')

def malas(request):
    template=loader.get_template('malas.html')
    context={ 'title': 'Mala Prueba'}
    return HttpResponse(template.render(context,request)) 

def logout_view(request):
    logout(request)
    return redirect('/')



def graficas(request):
    calibres = ['6', '10', '12', '14', '16', '18', '20', '22']
    data = {}
    fech = {}
    
    moth = datetime.now()
    

    for calibre in calibres:
        # Filtrar datos para el calibre actual
        datos = PullTest.objects.filter(calibre=calibre, fecha__month=moth.month,tipo="OK").values_list('presion', flat=True)

        
            # Convertir a lista de valores
        lista_datos = list(datos)
        if lista_datos:
            data[calibre] = lista_datos
           
        
        
  
    data_json = json.dumps(data)
    

    context = {
        'title': 'Gráficas',
        'calibres': list(data.keys()),
        'data_json': data_json,  
       
    }

    return render(request, 'graficas.html', context)
