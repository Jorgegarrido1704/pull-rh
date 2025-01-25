from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import ControlAlmacen,RegistroImpo
from django.template.loader import render_to_string
from datetime import date,timedelta,datetime
from django.contrib import messages
import openpyxl

# Create your views here.

def indexAlm(request):
    user=request.user
    template = loader.get_template('almacen/index.html')
    if user is not None and user.is_authenticated:
        datos = RegistroImpo.objects.filter(status='Pendiente').values('invoiceNum').distinct()
        if user.username == 'comercio':
            ultimosRegistros = RegistroImpo.objects.filter(status='Pendiente').values().order_by('-id_importacion')[:30]
        elif user.username == 'almacen':
            ultimosRegistros = RegistroImpo.objects.filter(status='Reg_almacen').values().order_by('-id_importacion')[:30]
        elif user.username == 'almaCali':
            ultimosRegistros = RegistroImpo.objects.filter(status='Reg_Calidad').values().order_by('-id_importacion')[:30]    
        
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
    if user is not None and user.is_authenticated:
        if request.method == 'POST':
            archivo = request.FILES.get('archivo')

            # Check if a file was uploaded
            if not archivo:
                messages.error(request, "No se seleccionó ningún archivo.")
                return redirect('/almacen/registro_importacion.html')

            try:
                # Load the Excel file
                workbook = openpyxl.load_workbook(archivo)
                print(f"Archivo recibido: {archivo.name}")

                # Select the sheet named "FACTURA"
                if "FACTURA" in workbook.sheetnames:
                    sheet = workbook["FACTURA"]
                else:
                    messages.error(request, "El archivo no contiene una hoja llamada 'FACTURA'.")
                    return redirect('/almacen/registro_importacion.html')

                # Read specific cells
                invoce = sheet['F4'].value
                dateinvoce = sheet['F5'].value

                # Convert date if needed
                if isinstance(dateinvoce, str):
                    try:
                        dateinvoce = datetime.strptime(dateinvoce, "%Y-%m-%d").date()
                    except ValueError:
                        messages.error(request, "El formato de la fecha en la celda F5 no es válido.")
                        return redirect('/almacen/registro_importacion.html')

                print(f"Invoice: {invoce}, Date: {dateinvoce}")

                # Iterate through rows starting from row 19
                for row in sheet.iter_rows(min_row=19,max_row=518, min_col=1, max_col=18,):
                    b = row[1].value  # mfcExterno
                    c = row[2].value  # mfcInterno
                    f = row[5].value  # qty
                    g = row[6].value  # UnitPrice
                    p = row[15].value  # supplier
                    q = row[16].value  # poImpo
                    r = row[17].value  # PrevioNum

                    # If the cell in column B is empty, stop processing
                    if not b:
                        break

                    print(f"Processing row: {b}, {c}, {f}, {g}, {p}, {q}, {r}")

                    # Create a new RegistroImpo entry
                    RegistroImpo.objects.create(
                        fechaDeMovimiento=date.today(),
                        invoiceNum=invoce,
                        fechaImpo=dateinvoce,
                        mfcExterno=b,
                        mfcInterno=c,
                        qty=f,
                        UnitPrice=g,
                        supplier=p,
                        PoImpo=q,
                        previoNum=r,
                        UserImpoCharge=user
                    )

                messages.success(request, "Datos importados exitosamente.")
                return redirect('/almacen/index.html')

            except Exception as e:
                # Log and display the error
                print(f"Error al procesar el archivo: {e}")
                messages.error(request, f"Error al procesar el archivo: {e}")
                return redirect('/almacen/registro_importacion.html')

        return render(request, 'almacen/registro_importacion.html')
    else:
        return redirect('/almacen/index.html')

def registrosRecords(request):
    user = request.user   
    if user is not None and user.is_authenticated:
        template = loader.get_template('almacen/registroCalidad.html') 
        datosimpo = RegistroImpo.objects.all().filter(status='Pendiente').values()
        context = {
            'datosimpo': datosimpo,
        }
        
        return HttpResponse(template.render(context, request))
        
