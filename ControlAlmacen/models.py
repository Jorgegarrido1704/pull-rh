from django.db import models

class ControlAlmacen(models.Model):
    idRegAlm = models.AutoField(primary_key=True)
    itIdInt = models.CharField(max_length=30)
    Qty = models.FloatField()
    MovType = models.CharField(max_length=30)
    UserReg= models.CharField(max_length=30)
    id_importacion= models.IntegerField(max_length=40)
    codUnic = models.CharField(max_length=80)
    comentario = models.CharField(max_length=250)
    
    class Meta:
        db_table = 'controlalmacen'
        
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