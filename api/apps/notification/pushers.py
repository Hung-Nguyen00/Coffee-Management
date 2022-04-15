from abc import ABC, abstractmethod
from typing import Optional

from fcm_django.models import FCMDevice

from apps.core.utils import get_logger
from apps.notification.services.message import NotificationMessage
from apps.notification.services.result import SendNotificationResult

logger = get_logger(__name__)


class Pusher(ABC):
    @abstractmethod
    def send(self, message: NotificationMessage, badge: Optional[int] = None) -> SendNotificationResult:
        raise NotImplementedError()


class FireBasePusher:
    @classmethod
    def get_user_devices(cls, user):
        if not user:
            return []
        return FCMDevice.objects.filter(user=user)

    def send(self, message: NotificationMessage, badge: Optional[int] = None) -> SendNotificationResult:
        user = message.user
        devices = self.get_user_devices(user)
        if not devices.exists():
            logger.debug(f"User {user} has no devices")
            return SendNotificationResult(success=False, error="ERROR: No devices")
        devices.send_message(title=message.title, body=message.content, badge=badge, data=message.data, sound="default")
        return SendNotificationResult(success=True)


class FakePusher(Pusher):
    def send(self, message: NotificationMessage, badge: Optional[int] = None) -> SendNotificationResult:
        logger.info(f"Fake Pusher: [{message.title}], [{message.content}], [{badge}]")
        return SendNotificationResult(True)
