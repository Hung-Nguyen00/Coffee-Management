from django.db import models
from django.db.models import Sum, F
from model_utils.models import TimeStampedModel, SoftDeletableModel

# Create your models here.


class Table(TimeStampedModel, SoftDeletableModel):
    code = models.CharField(max_length=3, unique=True, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["code"]
    
    def __str__(self):
        return self.code
    
    
class Order(TimeStampedModel, SoftDeletableModel):
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    paid = models.BooleanField(default=False)
    paid_datetime = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(Table, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.code
    
    @property
    def total_price(self):
        return self.order_detail.annotate(total=F("price") * F("amount")).aggregate(Sum("total"))["total__sum"]
    
    
    
class Menu(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    selling_price = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=5)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
    
class OrderTable(TimeStampedModel, SoftDeletableModel):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, related_name="order_detail")
    menu  = models.ForeignKey(Menu, blank=True, null=True, on_delete=models.CASCADE, related_name="drinking_order")
    price = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=5)
    amount = models.SmallIntegerField(default=1, null=True, blank=True)
    
    def __str__(self):
        return str(self.price * self.amount)
    
    @property
    def total_price(self):
        return self.price * self.amount
    