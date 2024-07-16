from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Herramental

from datetime import date,timedelta,datetime
from django.template.loader import render_to_string

def diarios(request):
    template = loader.get_template('herramental/diarios.html')
    content={
        'title': 'Golpes Diarios',
        
    }
    return HttpResponse(template.render(content,request))
def index(request):
    template = loader.get_template('herramental/index_herr.html')
    content={
        'title': 'Home',
        
    }
    return HttpResponse(template.render(content,request))
