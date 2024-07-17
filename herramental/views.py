from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Herramental,Golpes_diarios
from datetime import date,timedelta,datetime
from django.template.loader import render_to_string
from .form import RegistroHerramental,RegistroGolpes
from django.contrib.auth import logout
import datetime as dt


def diarios(request):
    today = dt.date.today().strftime('%d-%m-%Y')
    template = loader.get_template('herramental/diarios.html')
    golpes=Golpes_diarios.objects.all().values().order_by('-id').filter(fecha_reg=today)
    content={
        'title': 'Golpes Diarios',
        'golpes':golpes
    }
    return HttpResponse(template.render(content,request))

def index(request):
    user = request.user
    if user is not None and user.is_authenticated: 
        template = 'herramental/index_herr.html'
        today = dt.date.today().strftime('%d-%m-%Y')
        Gdiarios=Golpes_diarios.objects.all().values().order_by('-id').filter(fecha_reg__contains=today)
        preventiva = Herramental.objects.all().values().order_by('-id').filter(mantenimiento='falta')
        context = {
            'title': 'Home',
            'form': RegistroHerramental(),
            'golpes':Gdiarios,
            'preventiva':preventiva
        }
       
        if request.method == 'POST':
            form = RegistroHerramental(request.POST)
            if form.is_valid():
                terminal = form.cleaned_data['terminal'].upper()
                herramental = form.cleaned_data['herramental']
                golpesDiarios = form.cleaned_data['golpesDiarios']
                buscar = Herramental.objects.filter(terminal=terminal, herramental=herramental).first()
                
                if buscar:
                    if today == buscar.fecha_reg:
                        buscar.golpesDiarios += golpesDiarios
                        buscar.golpesTotales += golpesDiarios
                    else:
                        buscar.fecha_reg = today
                        buscar.golpesDiarios = golpesDiarios
                        buscar.golpesTotales += golpesDiarios

                    buscar.maquina = 'maquina'
                    if ((buscar.golpesTotales+golpesDiarios) / 5000) > buscar.totalmant:
                        buscar.totalmant = int(buscar.golpesTotales / 5000)
                        buscar.mantenimiento = 'falta1'
                    

                    buscar.save()
                    new_golpes=Golpes_diarios(
                        herramental=herramental,
                        terminal=terminal,
                        fecha_reg=today,
                        golpesDiarios=golpesDiarios
                    )
                    new_golpes.save()
                    return redirect('/herramental')
                else:
                    new_entry = Herramental(
                        herramental=herramental,
                        terminal=terminal,
                        fecha_reg=today,
                        golpesDiarios=golpesDiarios,
                        golpesTotales=golpesDiarios,  
                        maquina='maquina',
                        totalmant=int(golpesDiarios / 5000) if (golpesDiarios / 5000) < 1 else 1,
                        mantenimiento='ok' if (golpesDiarios / 5000) < 1 else 'falta1'
                    )
                    new_entry.save()
                    new_golpes=Golpes_diarios(
                    herramental=herramental,
                    terminal=terminal,
                    fecha_reg=today,
                    golpesDiarios=golpesDiarios
                    )
                    new_golpes.save()
                    
                    return redirect('/herramental')
                
            else:
                context['form'] = form  
        return render(request, template, context)
    else:
        return redirect('/')
def mantenimientos(request):
    template = loader.get_template('herramental/mantenimientos.html')
    diarios=Herramental.objects.all().values().order_by('-golpesTotales')
    content={
        'title': 'Mantenimientos',
        'diarios':diarios  
    }
    return HttpResponse(template.render(content,request))

def registrarGolpes(request):
    user = request.user
    if user is not None and user.is_authenticated: 
        today = dt.date.today().strftime('%d-%m-%Y') 
        if request.method == 'POST':
            form = RegistroHerramental(request.POST)
            if form.is_valid():
                terminal = form.cleaned_data['terminal'].upper()
                herramental = form.cleaned_data['herramental']
                cant = form.cleaned_data['cant']
                buscar = Herramental.objects.filter(terminal=terminal, herramental=herramental).first()
                
                if buscar:
                    if today == buscar.fecha_reg.strftime('%d-%m-%Y'):
                        buscar.golpesDiarios += cant
                        buscar.golpesTotales += cant
                    else:
                        buscar.fecha_reg = today
                        buscar.golpesDiarios = cant
                        buscar.golpesTotales += cant

                    buscar.maquina = 'maquina'
                    if (buscar.golpesTotales / 5000) < buscar.totalmant:
                        buscar.totalmant = int(buscar.golpesTotales / 5000)
                        buscar.mantenimiento = 'falta1'
                    else:
                        buscar.mantenimiento = 'ok'

                    buscar.save()
                else:
                    new_entry = Herramental(
                        herramental=herramental,
                        terminal=terminal,
                        fecha_reg=today,
                        golpesDiarios=cant,
                        golpesTotales=cant,  # Assuming it's a new entry
                        maquina='maquina',
                        totalmant=int(cant / 5000) if (cant / 5000) < 1 else 1,
                        mantenimiento='falta1' if (cant / 5000) < 1 else 'ok'
                    )
                    new_entry.save()
                
                return redirect('/herramental/index_herr')
        else:
            return redirect( '/herramental/index_herr') 
    else:
        return redirect('/login')  # or wherever you want to redirect unauthenticated users


def logout_view(request):
    logout(request)
    return redirect('/')            