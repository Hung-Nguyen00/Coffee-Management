from apps.staff.services.tasks_management import SendReportStaffEveryWeek
from apps.notification.services.manager import NotificationManager
from apps.staff.models import Staff, Schedule, ScheduleStaff
from apps.users.models import User
import json
import datetime

class SendingEmailStaffService:
    
    @staticmethod
    def sending_email_to_report_schedule_staff_income_everyweek():
        date = datetime.date.today() - datetime.timedelta(1)
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        schedules = Schedule.objects.filter(date_of_week__range=[start_week, end_week]).values_list("id", flat=True)
        staff = ScheduleStaff.objects.filter(schedule_id__in=schedules).select_related("staff")
        list_staff = []
        for t in staff:
            list_staff.append({
                "first_name": t.staff.first_name,
                "last_name": t.staff.last_name,
                "income": t.total_income_of_a_day,
            })
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

