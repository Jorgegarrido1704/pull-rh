from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ControlAlmacen
from django.template.loader import render_to_string


# Create your views here.

def indexAlm(request):
    template = loader.get_template('almacen/index.html')
    return HttpResponse(template.render())

    