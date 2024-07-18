from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Herramental,Golpes_diarios,Paros
from datetime import date,timedelta,datetime
from django.template.loader import render_to_string
from .form import RegistroHerramental,RegistroGolpes,NewHerramental,Paros_reg
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
        ahora = dt.datetime.now().strftime('%d-%m-%Y %H:%M')
        Gdiarios = Golpes_diarios.objects.filter(fecha_reg=today).order_by('-id')
        preventiva = Herramental.objects.filter(mantenimiento='falta').order_by('-id')
        paros=Paros.objects.all().filter(equipo='Bancos para terminales', finhora ='').order_by('-id')
        
        context = {
            'title': 'Home',
            'form': RegistroHerramental(),
            'NewHer': NewHerramental(),
            'Paros_reg': Paros_reg(),
            'golpes': Gdiarios,
            'preventiva': preventiva,
            'paros': paros,
            'error': '',
        }     
        if request.method == 'POST':
            form = RegistroHerramental(request.POST)
            NewHer = NewHerramental(request.POST)
            paro = Paros_reg(request.POST)
            if form.is_valid():
                terminal = form.cleaned_data['terminal'].upper()
                herramental = form.cleaned_data['herramental']
                golpesDiarios = form.cleaned_data['golpesDiarios']
                buscar = Herramental.objects.filter(terminal=terminal, herramental=herramental).first()
                
                if buscar:
                    if today == buscar.fecha_reg.strftime('%Y-%m-%d'):
                        buscar.golpesDiarios += golpesDiarios
                        buscar.golpesTotales += golpesDiarios
                    else:
                        buscar.fecha_reg = today
                        buscar.golpesDiarios = golpesDiarios
                        buscar.golpesTotales += golpesDiarios

                    buscar.maquina = 'maquina'
                    if (buscar.golpesTotales / 5000) >= buscar.totalmant:
                        buscar.totalmant = int(buscar.golpesTotales / 5000)
                        buscar.mantenimiento = 'falta1'
                    else:
                        buscar.mantenimiento = 'ok'

                    buscar.save()
                    new_golpes = Golpes_diarios(
                        herramental=herramental,
                        terminal=terminal,
                        fecha_reg=today,
                        golpesDiarios=golpesDiarios
                    )
                    new_golpes.save()
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
                    new_golpes = Golpes_diarios(
                        herramental=herramental,
                        terminal=terminal,
                        fecha_reg=today,
                        golpesDiarios=golpesDiarios
                    )
                    new_golpes.save()
                
                return redirect('/herramental')
            else:
                context['form'] = form
            
            if NewHer.is_valid():
                buscarExt = Herramental.objects.filter(herramental=NewHer.cleaned_data['herramental']).first()
                if buscarExt:
                    context['NewHer'] = NewHer
                    context['error'] = 'Ya existe'
                else:
                    herramental = NewHer.cleaned_data['herramental'].upper()
                    terminal = NewHer.cleaned_data['terminal'].upper()
                    new_entry = Herramental(
                        herramental=herramental,
                        terminal=terminal,
                        fecha_reg=today,
                        golpesDiarios=0,
                        golpesTotales=0,
                        maquina='Bodega_aplicadores',
                        totalmant=0,
                        mantenimiento='ok'
                    )
                    new_entry.save()
                    context['error'] = 'Nuevo herramental registrado exitosamente'
            else:
                context['NewHer'] = NewHer
            if paro.is_valid():
                fecha = paro.cleaned_data['fecha']
                herra = paro.cleaned_data['herra']
                dano = paro.cleaned_data['dano']
                quien = paro.cleaned_data['quien']
                atiende = paro.cleaned_data['atiende']
                buscarParos= Paros.objects.filter(fecha=fecha, nombreEquipo=herra, dano=dano, quien=quien).first()
                if  buscarParos:
                    if buscarParos.atiende == '':
                        buscarParos.atiende = atiende
                        buscarParos.inimant = ahora
                    else:
                        buscarParos.finhora = ahora
                    buscarParos.save()
                    redirect('/herramental')     
            else:
                context['Paros_reg'] = paro       
                        
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
