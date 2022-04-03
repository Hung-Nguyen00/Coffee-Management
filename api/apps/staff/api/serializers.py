from turtle import position
from rest_framework import serializers
from apps.staff.models import Staff, Position, ScheduleStaff, Schedule
from apps.staff.enums import SessionName
from datetime import datetime
from apps.staff.exceptions import ScheduleStaffExistException, SessionDoesNotExistException
import calendar

class PositionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(max_length=250)
    is_removed = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Position
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20, required=True)
    last_name  = serializers.CharField(max_length=30, required=True)
    phone = serializers.CharField(max_length=11, required=True)
    identity_card = serializers.CharField(max_length=20, required=True)
    pos_id = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), required=True, write_only=True)
    pos = PositionSerializer(read_only=True)
            
    class Meta:
        model = Staff
        fields = (
            "id", "first_name", "last_name", "phone", "identity_card", "pos_id",
            "pos", "income", "is_return_suit", "full_name"
        )
        

class ScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.CharField(max_length=10, required=True)
    date_of_week = serializers.DateField(required=True)
    
    class Meta:
        model = Schedule
        fields = ("id", "day_of_week", "date_of_week")


class ScheduleStaffUpdateSerializer(serializers.ModelSerializer):
    sessions = serializers.ListField(child=serializers.CharField(max_length=10), required=True)
            
    class Meta:
        model = ScheduleStaff
        fields = ("id", "staff", "schedule", "total_hours_of_a_day", "sessions")



class ScheduleStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source="staff", write_only=True, required=True)
    sessions = serializers.ListField(child=serializers.CharField(max_length=10), required=True)    
    date_of_week = serializers.DateField(required=True, write_only=True)
    total_income_of_a_day = serializers.SerializerMethodField()
    
    class Meta:
        model = ScheduleStaff
        fields = ("id", "staff", "schedule", "total_income_of_a_day",
                  "total_hours_of_a_day", "date_of_week", "sessions", "staff_id")
    
    @classmethod
    def get_total_income_of_a_day(cls, obj):
        return obj.total_income_of_a_day
    
    def validate_sessions(self, sessions):
        session_name = [SessionName.AFF, SessionName.MOR, SessionName.EVE]
        for session in sessions:
            if session not in session_name:
                raise SessionDoesNotExistException()
        return sessions
    
    def update(self, instance, validated_data):
        date = validated_data.pop("date_of_week")
        day_of_date = calendar.day_name[date.weekday()]
        schedule, created = Schedule.objects.get_or_create(date_of_week=date, defaults={"day_of_week": day_of_date})
        validated_data["schedule_id"] = schedule.id
        schedule_staff = super().update(instance, validated_data)
        return schedule_staff    
        
    def create(self, validated_data):
        date = validated_data.pop("date_of_week")
        day_of_date = calendar.day_name[date.weekday()]
        staff = validated_data["staff"]
        
        schedule, created = Schedule.objects.get_or_create(date_of_week=date, defaults={"day_of_week": day_of_date})
        validated_data["schedule_id"] = schedule.id
        check_staff_schedule = ScheduleStaff.objects.filter(schedule=schedule, staff=staff)
        if check_staff_schedule:
            raise ScheduleStaffExistException()
        schedule_staff = super(ScheduleStaffSerializer, self).create(validated_data)
        return schedule_staff
        