from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.core.utils import get_logger, get_now
from apps.users.api.serializers import UserSerializer
from apps.users.models import User
from apps.users.signals import user_avatar_updated_signal, user_signup_signal
from apps.users.tasks import create_thumbnail_task, send_create_oscar_user

logger = get_logger(__name__)


@receiver(user_signup_signal)
def user_signup_handler(sender, user: User, **kwargs):
    """
    Sign up new customer shop account
    :param sender:
    :param user:
    :param kwargs:
    :return:
    """
    data = UserSerializer(user).data
    data["username"] = user.username
    # send_create_oscar_user(data)


@receiver(user_avatar_updated_signal)
@receiver(user_signup_signal)
def create_avatar_thumbnail(sender, user: User, **kwargs):
    if user.avatar:
        transaction.on_commit(lambda: create_thumbnail_task.delay(user.pk))


@receiver(pre_save, sender=User)
def soft_delete_user(**kwargs):
    user = kwargs["instance"]
    if user.is_removed:
        timestamp = int(get_now().timestamp())
        user.email = f"deleted_{timestamp}_{user.email}"
