from apps.staff.services.tasks_management import SendReportStaffEveryWeek
from apps.notification.services.manager import NotificationManager
from apps.staff.models import Staff, Schedule, ScheduleStaff, IncomeHistory
from apps.users.models import User
import json
import datetime

class SendingEmailStaffService:
    
    def __init__(self, today):
        self.today = today
        self.year  = today.year
        self.month = today.month
        self.day   = today.day
    
    def sending_email_to_report_schedule_staff_income_everyweek(self):
        today          = self.today
        start_day_week = today - datetime.timedelta(today.weekday())
        end_day_week   = start_day_week + datetime.timedelta(6)
        schedules      = Schedule.objects.filter(date_of_week__range=[start_day_week, end_day_week]).values_list("id", flat=True)
        staff          = ScheduleStaff.objects.filter(schedule_id__in=schedules).select_related("staff")
        list_staff      = []
        list_his_income = []
        for t in staff:
            list_staff.append({
                "first_name": t.staff.first_name,
                "last_name": t.staff.last_name,
                "income": t.total_income_of_a_day,
            })
            list_his_income.append(IncomeHistory(schedule_staff=t, date_payment=today))
            
        IncomeHistory.objects.bulk_create(list_his_income)
        # staffs = Staff.objects.filter(schedulestaff__schedule_id__in=schedules).prefetch_related("schedulestaff_set")
        # get_staff_fields = [
        #     {"first_name":staff.first_name, "last_name": staff.last_name, 
        #      "income": staff.schedulestaff_set.first().total_income_of_a_day}
        #     for staff in staffs
        # ]
        # print(get_staff_fields)
        users_admin = User.objects.filter(is_superuser=True, is_active=True)
        for user in users_admin:
            NotificationManager.send(
                SendReportStaffEveryWeek(user=user, staff=list_staff)
            )

