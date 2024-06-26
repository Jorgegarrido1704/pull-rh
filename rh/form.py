from django import forms
from .models import Vacaciones,RegistroVacaciones

class RegistroFrom(forms.ModelForm):
    choice_empleado=[('','')]
    for x in Vacaciones.objects.all().values():
        choice_empleado.append((x['id_empleado'],x['id_empleado']),)
    choice_status=[
        ('',''),
        ('Pendiente','Pendiente'),
    ]
    id_empleado=forms.ChoiceField(choices=choice_empleado,widget=forms.Select(attrs={'class':'form-control','id':'id_empleado', 'onchange':'datos()'}))
    fecha_de_solicitud=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD','type':'date'}))
    estatus=forms.ChoiceField(choices=choice_status,widget=forms.Select(attrs={'class':'form-control'}))
    dias_solicitados=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model=RegistroVacaciones
        fields=['id_empleado','fecha_de_solicitud','estatus','dias_solicitados']
        labels={
            'id_empleado':'Empleado',
            'fecha_de_solicitud':'Fecha de Solicitud',
            'estatus':'Estatus',
            'dias_solicitados':'Dias Solicitados',  
        }