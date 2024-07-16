from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Herramental,Golpes_diarios

from datetime import date,timedelta,datetime
from django.template.loader import render_to_string

def diarios(request):
    template = loader.get_template('herramental/diarios.html')
    golpes=Golpes_diarios.objects.all().values().order_by('-id')
    content={
        'title': 'Golpes Diarios',
        'golpes':golpes
    }
    return HttpResponse(template.render(content,request))
def index(request):
    template = loader.get_template('herramental/index_herr.html')
    content={
        'title': 'Home',
    }
    return HttpResponse(template.render(content,request))

def mantenimientos(request):
    template = loader.get_template('herramental/mantenimientos.html')
    diarios=Herramental.objects.all().values().order_by('id')
    content={
        'title': 'Mantenimientos',
        'diarios':diarios  
    }
    return HttpResponse(template.render(content,request))