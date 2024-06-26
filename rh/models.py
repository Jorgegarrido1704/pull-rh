from django.db import models
from datetime import date

class Vacaciones(models.Model):
    id_empleado = models.CharField(max_length=100)
    numero_empleado = models.IntegerField()
    fecha_de_entrada = models.DateField()
    fecha_de_corte = models.DateField(default=date.today)
    dias_utilizados = models.IntegerField(default=0)
    ultima_fecha_de_solicitud = models.DateField()

    def __str__(self):
        return self.id_empleado

    class Meta:
        db_table = 'vacaciones'

class RegistroVacaciones(models.Model):
    id_empleado = models.CharField(max_length=100)
    fecha_de_solicitud = models.DateField()
    estatus = models.CharField(max_length=100)
    dias_solicitados = models.IntegerField()

    def __str__(self):
        return str(self.id_empleado)

    class Meta:
        db_table = 'registro_vacaciones'

    
