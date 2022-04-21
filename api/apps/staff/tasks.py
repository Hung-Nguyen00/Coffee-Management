from datetime import datetime

from celery.schedules import crontab

from apps.core.celery import app

from apps.staff.services.sending_email import SendingEmailStaffService


result = SendingEmailStaffService(datetime.today())

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Execute every weekdays at 1:00 AM
    sender.add_periodic_task(crontab(hour=18, day_of_week=1), sending_email_income_employee.s())
    
    
@app.task()   
def sending_email_income_employee():
    """ Sending Imcome of staff to admin"""
    result.sending_email_to_report_schedule_staff_income_everyweek()
