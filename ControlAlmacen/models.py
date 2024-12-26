from django.db import models

class ControlAlmacen(models.Model):
    id_control = models.AutoField(primary_key=True)
    id_empleado = models.IntegerField()
    fecha_registro = models.CharField(max_length=30)
    mnfint= models.CharField(max_length=30)
    mnfext= models.CharField(max_length=30)
    cantidad = models.FloatField()
    impoNum= models.CharField(max_length=30)
    impoFecha= models.CharField(max_length=30)
    codigoUnico= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=200)
    
    class Meta:
        db_table = 'control_almacen'
        
    def __str__(self):
        return self.impoNum
    
    
    
