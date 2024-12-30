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

class RegistroImpo(models.Model):
    id_importacion = models.AutoField(primary_key=True)
    fechaDeMovimiento = models.CharField(max_length=10)
    mfcInterno = models.CharField(max_length=40)
    mfcExterno = models.CharField(max_length=40)
    qty = models.FloatField()
    UnitPrice = models.FloatField()
    supplier = models.CharField(max_length=40)
    PoImpo = models.CharField(max_length=30)
    previoNum = models.CharField(max_length=40)
    invoiceNum = models.CharField(max_length=40)
    fechaImpo = models.CharField(max_length=10)
    status = models.CharField(max_length=30, default='Pendiente')
    UserImpoCharge = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'inv'
        
    def __str__(self):
        return self.PoImpo