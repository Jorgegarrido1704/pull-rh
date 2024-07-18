from django.db import models

# Create your models here.

class Herramental(models.Model):
    herramental = models.CharField(max_length=30)
    terminal = models.CharField(max_length=30)
    fecha_reg = models.CharField(max_length=30)
    golpesDiarios = models.IntegerField(default=0)
    golpesTotales= models.IntegerField(default=0)
    maquina = models.CharField(max_length=80)
    totalmant = models.IntegerField(default=0)
    mantenimiento = models.CharField(max_length=6)
    
    class Meta:
        db_table = "mant_golpes_diarios"
        
    def __str__(self):
        return self.herramental
 
class Golpes_diarios(models.Model):
    herramental = models.CharField(max_length=30)
    terminal = models.CharField(max_length=30)
    fecha_reg = models.CharField(max_length=30)
    golpesDiarios = models.IntegerField(default=0)
    
    class Meta:
        db_table = "mant_golpes"
        
    def __str__(self):
        return self.herramental
    
class Paros(models.Model):
    fecha = models.CharField(max_length=30)
    equipo = models.CharField(max_length=80)
    nombreEquipo = models.CharField(max_length=80)
    dano = models.CharField(max_length=80)
    quien = models.CharField(max_length=80)
    area = models.CharField(max_length=80)
    atiende = models.CharField(max_length=80)
    trabajo = models.CharField(max_length=80)
    Tiempo = models.CharField(max_length=80)
    inimant = models.CharField(max_length=80)
    finhora = models.CharField(max_length=80)
    class Meta:
        db_table = "registro_paro"
        
    def __str__(self):
        return self.equipo    