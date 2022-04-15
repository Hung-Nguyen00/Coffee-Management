import celery

from apps.notification.services.task import send_notification_task_handler


class SendQueuedMessageTask(celery.Task):
    ignore_result = True

    def run(self, message_id: str, *args, **kwargs):
        send_notification_task_handler(message_id=message_id)
