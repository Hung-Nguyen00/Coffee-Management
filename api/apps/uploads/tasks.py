from datetime import datetime, timedelta

from celery.schedules import crontab

from apps.core.celery import app
from apps.uploads.enums import FileState
from apps.uploads.models import UploadFile
from apps.uploads.settings import app_settings as settings


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=12), auto_delete_task.s())


@app.task
def auto_delete_task():
    print("Automated Delete Record File Not Used Task is end ....")
    time_space = datetime.now() - timedelta(hours=settings.TIME_TO_DELETE_UPLOAD_FILE)
    UploadFile.objects.filter(status=FileState.NEW, created__lt=time_space).delete()
    print("Automated Delete Record File Not Used Task is successfully ....")
