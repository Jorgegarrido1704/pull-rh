from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Vacaciones,RegistroVacaciones
from .form import RegistroFrom
from datetime import date,timedelta,datetime
from django.template.loader import render_to_string
import openpyxl
from django.core.files.storage import FileSystemStorage
from openpyxl import Workbook
from io import BytesIO




def index(request):
    templete=loader.get_template('rh/index.html')
    vacaciones=RegistroVacaciones.objects.all().values()
    
    data=[0,0,0,0,0,0,0,0,0,0,0,0]
    for vac in RegistroVacaciones.objects.all().values():
        fecha=int(vac['fecha_de_solicitud'].month)
        data[fecha-1]+=1
        
    
    labels=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    context={
        'vacaciones':vacaciones,
        'title':'Registros_vacacioens',
        'labels':labels,
        'data':data
        
    }
    return HttpResponse(templete.render(context,request))

def vacaciones(request):
    template=loader.get_template('rh/registroVac.html')
    form=RegistroFrom()
    context={
        'form':form
    }
    if request.method=='POST':
        form=RegistroFrom(request.POST)
        if form.is_valid():
            empleadoupdate=Vacaciones.objects.get(id_empleado=form.cleaned_data['id_empleado'])
            empleadoupdate.dias_utilizados+=form.cleaned_data['dias_solicitados']
            empleadoupdate.ultima_fecha_de_solicitud=date.today()
            empleadoupdate.save()
            
            form.save()

    return HttpResponse(template.render(context,request))
    
def vacaciones_detalles(request, id_empleado):
    vac = get_object_or_404(Vacaciones, id_empleado=id_empleado)  
    Antiguedad = date.today() - vac.fecha_de_entrada
    ant = round(Antiguedad.days / 365,0)
    if(ant==1):
        dias=12
    elif(ant==2):
        dias=14
    elif(ant==3):
        dias=16
    elif(ant==4 ):
        dias=18
    elif(ant==5):
        dias=20
    elif (ant>=6 and ant<=10):
        dias=22
    elif (ant>=11 and ant<=15):
        dias=24
    elif (ant>=16 and ant<=20):
        dias=26
    elif(ant>=21 and ant<=25):
        dias=28
    elif(ant>=26 and ant<=30):
        dias=30
    elif(ant>=31 and ant<=35):
        dias=32                            
    
    if(vac.fecha_de_corte>vac.fecha_de_entrada):
        dispinibles= date.today() - vac.fecha_de_corte
        disp=round(dias*dispinibles.days / 365,0)-int(vac.dias_utilizados)
        
                     
    
    
    data = {
        'vac': {
            'id_empleado': vac.id_empleado,
            'numero_empleado': vac.numero_empleado,
            'fecha_de_entrada': vac.fecha_de_entrada,
            'antiguedad': ant,
            'dias_por_ano': dias,
            'fecha_de_corte': vac.fecha_de_corte,
            'dias_disponibles': disp,
            'dias_utilizados': vac.dias_utilizados,
            'ultima_fecha_de_solicitud': str(vac.ultima_fecha_de_solicitud)
        }
    }
    return JsonResponse(data)

def reportes(request, numero_empleado):
    numEmp = get_object_or_404(Vacaciones, numero_empleado=numero_empleado)
    registros = RegistroVacaciones.objects.filter(id_empleado=numEmp.id_empleado).order_by('-fecha_de_solicitud')

    datos = {
        'rep': [{
            
            'id_empleado': reg.id_empleado,
            'fecha_de_solicitud': str(reg.fecha_de_solicitud),
            'dias_solicitados': reg.dias_solicitados,
            'estatus': reg.estatus
        } for reg in registros]
    }
    return JsonResponse(datos)


def generate_pdf(request):
    if request.method == "GET":
        id_empleado = request.GET.get('id_emp', 'Unknown')
        fecha = request.GET.get('fecha', 'Unknown')
        dias_pedidos = request.GET.get('dias', 'Unknown')
        vac=Vacaciones.objects.get(id_empleado=id_empleado)
        dias_mas=int(dias_pedidos)
        fecha_fin = datetime.strptime(fecha, '%Y-%m-%d').date() + timedelta(days=dias_mas)
        
        Antiguedad = date.today() - vac.fecha_de_entrada
        ant = round(Antiguedad.days / 365,0)
        if(ant==1):
            dias=12
        elif(ant==2):
            dias=14
        elif(ant==3):
            dias=16
        elif(ant==4 ):
            dias=18
        elif(ant==5):
            dias=20
        elif (ant>=6 and ant<=10):
            dias=22
        elif (ant>=11 and ant<=15):
            dias=24
        elif (ant>=16 and ant<=20):
            dias=26
        elif(ant>=21 and ant<=25):
            dias=28
        elif(ant>=26 and ant<=30):
            dias=30
        elif(ant>=31 and ant<=35):
            dias=32                            
        
        if(vac.fecha_de_corte>vac.fecha_de_entrada):
            dispinibles= date.today() - vac.fecha_de_corte
            disp=round(dias*dispinibles.days / 365,0)-int(vac.dias_utilizados)
        
        
        wb_existente = openpyxl.load_workbook(r'C:\Users\Jorge Garrido\OneDrive\Escritorio\production\rh\vaciones.xlsx')
        hoja_existente = wb_existente.active
        celda = hoja_existente['B8']
        celda.value = id_empleado
        celda = hoja_existente['K8']
        celda.value =   vac.numero_empleado
        celda = hoja_existente['M8']
        celda.value =   ant
        celda = hoja_existente['B11']
        celda.value =   'Operador'
        celda = hoja_existente['E11']
        celda.value =   vac.ultima_fecha_de_solicitud
        celda = hoja_existente['I11']
        celda.value =   dias
        celda = hoja_existente['K11']
        celda.value =   dias_pedidos
        celda = hoja_existente['M11']
        celda.value =   disp
        celda = hoja_existente['D13']
        celda.value =   fecha
        celda = hoja_existente['d15']
        celda.value =   fecha_fin
        
        buffer = BytesIO()
        wb_existente.save(buffer)
        buffer.seek(0)
        
        # Preparar la respuesta HTTP con el archivo modificado
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Vacaciones_de_{}.xlsx"'.format(id_empleado)
        
        return response