from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .models import ControlAlmacen,RegistroImpo
from django.template.loader import render_to_string
from datetime import date
from django.contrib import messages
import openpyxl

# Create your views here.

def indexAlm(request):
    user=request.user
    
    if user is not None and user.is_authenticated:
        return render(request, 'almacen/index.html')
    else:
        return redirect('/')

def registroimpo(request):
    user = request.user
    if user is not None and user.is_authenticated:
        if request.method == 'POST':
            archivo = request.FILES.get('archivo')

            if not archivo:
                messages.error(request, "No se seleccionó ningún archivo.")
                return redirect('almacen/registro_importacion.html')

            try:
                workbook = openpyxl.load_workbook(archivo)

                # Seleccionar la hoja llamada "FACTURA"
                if "FACTURA" in workbook.sheetnames:
                    sheet = workbook["FACTURA"]
                else:
                    messages.error(request, "El archivo no contiene una hoja llamada 'FACTURA'.")
                    return redirect('almacen/registro_importacion.html')

                # Leer las celdas específicas
                invoce = sheet['F4'].value
                dateinvoce = sheet['F5'].value

                # Iterar desde la fila 19 hacia abajo
                for row in sheet.iter_rows(min_row=19):
                    b, c, f, g, p, q, r = (row[1].value, row[2].value, row[5].value, row[6].value,
                                           row[15].value, row[16].value, row[17].value)

                    # Si la celda B está vacía, detener
                    if not b:
                        break

                    # Guardar en el modelo
                    RegistroImpo.objects.create(
                        fechaDeMovimiento=date.today(),
                        invoiceNum=invoce,
                        fechaImpo=dateinvoce,
                        mfcExterno=b,
                        mfcInterno=c,
                        qty=f,
                        UnitPrice=g,
                        supplier=p,
                        poImpo=q,
                        PrevioNum=r,
                        UserImpoCharge=user
                    )
                    RegistroImpo.save()

                messages.success(request, "Datos importados exitosamente.")
                return redirect('almacen/registro_importacion.html')

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
                return redirect('almacen/registro_importacion.html')
        return render(request, 'almacen/registro_importacion.html')
    else:
        return redirect('/')