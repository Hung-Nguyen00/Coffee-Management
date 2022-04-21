from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from apps.equipments.enums import EquipmentStatus, MaterialStatus
from django.db.models import Q, Sum

# Create your models here.

class Equipment(TimeStampedModel, SoftDeletableModel):
    name     = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    buying_price = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=11)
    status   = models.CharField(max_length=10, choices=EquipmentStatus.choices(), null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ('name',)
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"
        
    def __str__(self):
        return self.name

    @property
    def total_buying_price(self):
        return str(self.quantity * self.buying_price)
    
    
class Supplier(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=50, null=True, blank=True)    
    address = models.CharField(max_length=150, null=True, blank=True)    
    phone = models.CharField(max_length=11, null=True, blank=True)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name    
    
    
class Material(TimeStampedModel, SoftDeletableModel):
    name   = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    unit   = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, choices=MaterialStatus.choices())
    
    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ('name',)
        verbose_name = "Material"
        verbose_name_plural = "Materials"
    
    
    def __str__(self):
        return self.name
    

class Bill(TimeStampedModel, SoftDeletableModel):
    supplier    = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.SET_NULL)
    date_input  = models.DateTimeField(null=True, blank=True)
    is_payment  = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-date_input',)
    
    @property
    def total_money_bill(self):
        if self.bill_details.exists():
            return sum(detail.total_money for detail in self.bill_details.all())
        return 0
    
        
class BillDetail(TimeStampedModel, SoftDeletableModel):
    bill      = models.ForeignKey(Bill, blank=True, null=True, on_delete=models.CASCADE, related_name="bill_details")
    materials = models.ForeignKey(Material, blank=True, null=True, on_delete=models.CASCADE)
    amount    =  models.FloatField(default=0.0, null=True, blank=True)
    buying_price = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=11)
    
    @property
    def total_money(self):
        return self.amount * float(self.buying_price)