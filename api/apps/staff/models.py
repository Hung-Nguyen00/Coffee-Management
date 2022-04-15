from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.staff.enums import SessionName
from model_utils.models import TimeStampedModel, SoftDeletableModel
from apps.staff.contains import TOTAL_HOURS_OF_MORNING, TOTAL_HOURS_OF_AFTERNOON, TOTAL_HOURS_OF_EVENING

# Create your models here.
class Position(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Staff(TimeStampedModel, SoftDeletableModel):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(default="", blank=True, max_length=12)
    identity_card = models.CharField(max_length=20, null=True, blank=True)
    bod = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    is_return_suit = models.BooleanField(default=True)
    income = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, default=0)
    pos = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.last_name + " " + self.first_name
    
    @property
    def full_name(self):
        return self.last_name + " " + self.first_name


class Schedule(TimeStampedModel, SoftDeletableModel):
    date_of_week = models.DateField(null=True, blank=True)
    day_of_week = models.CharField(null=True, blank=True, max_length=10) 


class ScheduleStaff(TimeStampedModel, SoftDeletableModel):
    staff = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, null=True, blank=True, on_delete=models.CASCADE)
    sessions = ArrayField(models.CharField(max_length=10, null=True, blank=True, choices=SessionName.choices()))
    total_hours_of_a_day = models.PositiveSmallIntegerField(null=True, blank=True, default=8)
    total_hours_off_a_day = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        return str(self.staff)
    
    @property
    def total_income_of_a_day(self): 
        if self.staff:
            return self.total_hours_of_a_day * int(self.staff.income)
        return None
    
    def save(self, *args, **kwargs):
        self.total_hours_of_a_day = 0 - self.total_hours_off_a_day
        for sessions in self.sessions:
            if sessions == SessionName.MOR:
                self.total_hours_of_a_day += TOTAL_HOURS_OF_MORNING
            if sessions == SessionName.AFF:
                self.total_hours_of_a_day += TOTAL_HOURS_OF_AFTERNOON
            if sessions == SessionName.EVE:
                self.total_hours_of_a_day += TOTAL_HOURS_OF_EVENING
                
        super(ScheduleStaff, self).save(*args, **kwargs) 
        

class IncomeHistory(TimeStampedModel, SoftDeletableModel):
    schedule_staff = models.ForeignKey(ScheduleStaff, null=True, blank=True, on_delete=models.SET_NULL)
    is_payment = models.BooleanField(default=False)
    date_payment = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.date_payment