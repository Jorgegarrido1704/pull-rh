from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .models import ControlAlmacen
from django.template.loader import render_to_string



# Create your views here.

def indexAlm(request):
    user=request.user
    
    if user is not None and user.is_authenticated:
        return render(request, 'almacen/index.html')
    else:
        return redirect('/')

    