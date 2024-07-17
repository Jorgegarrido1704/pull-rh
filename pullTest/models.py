from django.db import models

# Create your models here.
class PullTest(models.Model):
    fecha = models.CharField(max_length=30)
    calibre  = models.IntegerField(default=0)
    Cliente = models.CharField(max_length=80)
    Num_part = models.CharField(max_length=50)
    wo = models.CharField(max_length=6)
    presion = models.FloatField(default=0.00)
    forma = models.CharField(max_length=80)
    cont = models.CharField(max_length=80)
    quien = models.CharField(max_length=80)
    val = models.CharField(max_length=80,default=" ")
    tipo = models.CharField(max_length=4,default=" ") 
    
    class Meta:
        db_table = "registro_pull"

    def __str__(self):
        return self.Num_part
    
    
    
