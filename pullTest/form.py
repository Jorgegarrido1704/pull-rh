# myapp/forms.py
from django import forms
from .models import PullTest

class RegistroTest(forms.ModelForm):
    FORMA_CHOICES = [
        ('',''),
        ('Banco', 'Banco'),
        ('Pinza', 'Pinza'),
        ('Canon', 'Cañon'),
        ('Corte', 'Corte'),
        ('Empalme', 'Empalme'),
    ]

    CLIENTE_CHOICES = [
        ('',''),
        ('BERGSTROM', 'BERGSTROM'),
        ('CALIFORNIA', 'EL DORADO CALIFORNIA'),
        ('UTILIMASTER', 'UTILIMASTER'),
        ('NILFISK', 'NILFISK'),
        ('SHYFT', 'SHYFT'),
        ('TICO', 'TICO MANUFACTURING'),
        ('ATLAS', 'ATLAS COPCO'),
        ('KALMAR', 'KALMAR'),
        ('MODINE', 'MODINE'),
        ('BLUE BIRD', 'BLUE BIRD'),
        ('FOREST RIVER', 'FOREST RIVER'),
        ('CAPACITY', 'CAPACITY'),
        ('PHOENIX', 'PHOENIX'),
        ('COLLINS', 'COLLINS'),
        ('SPARTAN', 'SPARTAN'),
        ('PROTERRA CALIFORNIA', 'PROTERRA CALIFORNIA'),
        ('DUR-A-LIFT','DUR-A-LIFT'),
    ]
    CALIBRE_CHOICES = [
    ('',''),
    (6, '6'),
    (10, '10'),
    (12, '12'),
    (14, '14'),
    (16, '16'),
    (18, '18'),
    (20, '20'),
    (22, '22'),
]
    Cliente = forms.ChoiceField(choices=CLIENTE_CHOICES, widget=forms.Select(attrs={'class': 'form-select','required': 'required'}))
    calibre = forms.ChoiceField(choices=CALIBRE_CHOICES, widget=forms.Select(attrs={'class': 'form-control','required': 'required'}))
    forma = forms.ChoiceField(choices=FORMA_CHOICES, widget=forms.Select(attrs={'class': 'form-select','required': 'required'}))
    Num_part = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))
    wo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required', 'placeholder': '006666'}))
    cont = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required', 'placeholder': 'TT2-152 o empalme 5'}))
    presion = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control','required': 'required', 'step': '0.01'}))
    quien = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))

    class Meta:
        model = PullTest
        fields = ['Cliente', 'Num_part', 'calibre','wo', 'cont', 'forma', 'presion', 'quien']
        labels = {
            'Num_part': 'Numero de parte',
            'wo': 'Work Order',
            'cont': 'Terminal o No° empalme',
            'forma': 'Forma de aplicacion',
            'presion': 'Presion (Lb)',
            'quien': 'Quien Registra',
            'calibre': 'Calibre',
        }
