from django import forms
from .models import ControlAlmacen

class ControlRegistroNormInput(forms.ModelForm):
    employees_choices=[
        ('', ''),
        ('Andrea Pacheco', 'Andrea Pacheco'),
        ('Erick Nunez', 'Erick Nunez'),
        ('Marisol Perez', 'Marisol Perez'),
        ('Didier Maldonado', 'Didier Maldonado'),
    ]
    id_empleado = forms.ChoiceField(choices=employees_choices, widget=forms.Select(attrs={'class': 'form-select','required': 'required'}))
    