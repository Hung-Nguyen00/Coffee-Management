import uuid

from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel

User = get_user_model()


class AppleApp(TimeStampedModel):
    APPLE = "APPLE"
    APPS = ((APPLE, "Apple"),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app = models.CharField(choices=APPS, max_length=20, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    apple_id_client = models.CharField(max_length=200, null=True, blank=True)
    apple_id_team = models.CharField(max_length=200, null=True, blank=True)
    apple_id_key = models.CharField(max_length=200, null=True, blank=True)
    apple_private_key = models.TextField(null=True, blank=True)


class AppleAccount(TimeStampedModel):
    apple_id = models.CharField(verbose_name="Apple user id", max_length=250, primary_key=True)
    email = models.CharField(verbose_name="Apple email", max_length=250, default=None, null=True, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
