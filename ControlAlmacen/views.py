from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import ControlAlmacen,RegistroImpo
from django.template.loader import render_to_string
from datetime import date,datetime
from django.contrib import messages
import openpyxl
import pandas as pd

# Create your views here.

def indexAlm(request):
    user=request.user
    template = loader.get_template('almacen/index.html')
    if user is not None and user.is_authenticated:
        datos = RegistroImpo.objects.filter(status='Pendiente').values('invoiceNum').order_by('-invoiceNum').distinct()[:10]
        if user.username == 'comercio' or user.username == 'Indihra_M' or user.username == 'Rocio_F' or user.username == 'Favian_M' or user.username == 'Fatima_S':
            ultimosRegistros = RegistroImpo.objects.filter(status='Pendiente').values().order_by('-id_importacion')[:100]
        elif user.username == 'almacenUser':
            ultimosRegistros = ControlAlmacen.objects.filter(MovType='Entrada By Reg_almacen').values().order_by('-idRegAlm')[:30]
        elif user.username == 'calidadAlm':
            ultimosRegistros = ControlAlmacen.objects.filter(MovType='Entrada By Reg_Calidad').values().order_by('-idRegAlm')[:30]    
        
        template = loader.get_template('almacen/index.html')
        context = {
           'ultimosRegistros': ultimosRegistros,
            'datos': datos,
            'user': user
            
        }
        return HttpResponse(template.render(context, request))

    else:
        return redirect('/')


def registroimpo(request):
    user = request.user
    if not user or not user.is_authenticated:
        return redirect('/')
    if request.method != 'POST':
        return render(request, 'almacen/registro_importacion.html')

    archivo = request.FILES.get('archivo')
    invoice = request.POST.get('invoice')
    date_invoice = request.POST.get('dateinvoce')

    if not archivo:
        messages.error(request, "No se seleccionó ningún archivo.")
        return redirect('indexAlm')

    try:
        df = pd.read_excel(
        archivo,
        skiprows=17,
        nrows=533,  # 550 - 17 = 533 rows to read
        usecols=[1,2,5,6,17,18,19], # Read columns from 1 to 18
        names=[
            'Model Number', 'Customer Part #', 'Qty', 'Unit Price',
             'Supplier', 'PO #', 'PREVIO'
            ]
    )

# Print the columns to verify
        print(df.columns)

# Iterate through the rows of the DataFrame
        for _, row in df.iterrows():
    # Unpack the row values
            b, c, f, g, r, s, t = row.values[:7]  # Only unpack the expected 7 columns

            # Skip processing if 'Model Number' (b) is null or empty
            if pd.isna(b) or b == "":
                print("Skipping row with empty Model Number")
                continue

            print(f"Processing row: {b}, {c}, {f}, {g}, {r}, {s}, {t}")

    # Create a new record in RegistroImpo
            RegistroImpo.objects.create(
                fechaDeMovimiento=date.today(),
                invoiceNum=invoice,
                fechaImpo=date_invoice,
                mfcExterno=b,
                mfcInterno=c,
                qty=f,
                UnitPrice=g,
                supplier=r,
                PoImpo=s,
                previoNum=t,
                UserImpoCharge=user
            )

        messages.success(request, "Datos importados exitosamente.")
        return redirect('indexAlm')

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        messages.error(request, f"Error al procesar el archivo: {e}")
        return redirect('indexAlm')




def registrosRecords(request):
    user = request.user   
    accept = request.POST.get('idAccept')
    mfcInterno = request.POST.get('mfcInterno')
    qty = request.POST.get('qty')
    coment = request.POST.get('coment')
    
    if user is not None and user.is_authenticated:
        if user.username == 'almacenUser':
            regStatus='Reg_almacen'
        elif user.username == 'calidadAlm':
            regStatus='Reg_Calidad'
        if request.method == 'POST':
            if accept is not None or accept != '': 
                RegistroImpo.objects.filter(id_importacion=accept).update(status=regStatus)
                ControlAlmacen.objects.create(
                    fechaMov = date.today().strftime('%Y-%m-%d'),
                    itIdInt = mfcInterno,
                    Qty = qty,
                    MovType = 'Entrada By ' + regStatus ,
                    UserReg = user.username,
                    id_importacion = accept,
                    codUnic = date.today().strftime('%y%m%d-') + mfcInterno +'-#id' + str(accept)+'#-'+user.username,
                    comentario = coment
                    )
                messages.success(request, "Data updated successfully.")
                return redirect('registroMovimiento')
            
        template = loader.get_template('almacen/registroCalidad.html')
        datosimpo = RegistroImpo.objects.all().filter(status='Pendiente').values()
        context = {
                'datosimpo': datosimpo,
            }
        return HttpResponse(template.render(context, request))   
    else:
        return redirect('/') 
       
