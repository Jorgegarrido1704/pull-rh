from django.db import models

# Create your models here.

class Herramental(models.Model):
    herramental = models.CharField(max_length=30)
    terminal = models.CharField(max_length=30)
    fecha_reg = models.DateField(auto_now_add=True)
    golpesDiarios = models.IntegerField(default=0)
    golpesTotales= models.IntegerField(default=0)
    maquina = models.CharField(max_length=80)
    totalmant = models.IntegerField(default=0)
    
    class Meta:
        db_table = "mant_golpes_diarios"
        
    def __str__(self):
        return self.herramental