# myapp/forms.py
from django import forms
from .models import Herramental,Golpes_diarios

class RegistroHerramental(forms.ModelForm):
    
    choiceHerramental = Herramental.objects.all().values('herramental')
    FORMA_CHOICES = [
        ('', ''),
    ]
    for item in choiceHerramental:
        FORMA_CHOICES.append((item['herramental'], item['herramental']),)
    herramental = forms.ChoiceField(choices=FORMA_CHOICES, widget=forms.Select(attrs={'class': 'form-select','required': 'required'}))
    terminal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))
    golpesDiarios = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','required': 'required', 'placeholder': '0'}))
   
    class Meta:
        model = Herramental
        fields = ['herramental', 'terminal', 'golpesDiarios']
        labels = {
            'herramental': 'Herramiental',
            'terminal': 'Terminal',
            'golpesDiarios': 'Golpes Diarios',
            
        }

class RegistroGolpes(forms.ModelForm):
    herramental = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))
    terminal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))
    fecha_reg = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))
    golpesDiarios = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','required': 'required', 'placeholder': '0'}))
    
    class Meta:
        model = Golpes_diarios
        fields = ['herramental', 'terminal', 'fecha_reg', 'golpesDiarios']
        labels = {
            'herramental': 'Herramiental',
            'terminal': 'Terminal',
            'fecha_reg': 'Fecha de Registro',
            'golpesDiarios': 'Golpes Diarios',
        }