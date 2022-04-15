import uuid
from typing import Optional

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel

from apps.core import utils
from apps.notification import choices


class Category(TimeStampedModel):
    UNCATEGORIZED = "Uncategorized"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @classmethod
    def get_or_crate_default_category(cls):
        category, _ = Category.objects.get_or_create(name=Category.UNCATEGORIZED)
        return category


class Message(TimeStampedModel, SoftDeletableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="actor",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="receiver",
        on_delete=models.CASCADE,
    )

    topic = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    content = models.CharField(max_length=250, null=True, blank=True)
    template = models.CharField(max_length=250, null=True, blank=True, help_text="Message template")
    status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=choices.MESSAGE_STATUS_CHOICES,
        default=choices.MESSAGE_STATUS_QUEUED,
    )
    payload = models.JSONField(null=True, blank=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    visible = models.BooleanField(default=True, help_text="Visible to user?")

    """
    Generic foreign keys to other models
    """
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="content_object",
        null=True,
        blank=True,
    )
    object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    """
    Generic foreign keys to other models
    """
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="target_object",
        null=True,
        blank=True,
    )
    target_id = models.UUIDField(null=True, blank=True)
    target_object = GenericForeignKey("target_type", "target_id")

    memo = models.CharField(max_length=250, null=True, blank=True, help_text="Internal Notes")

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["created"]),
            models.Index(fields=["user", "visible", "is_removed"]),
        ]

        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.content

    def is_queued(self) -> bool:
        return self.status == choices.MESSAGE_STATUS_QUEUED

    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_sent(self):
        self.status = choices.MESSAGE_STATUS_SENT
        self.sent_date = utils.get_utc_now()
        self.save()

    def mark_as_failed(self, error: Optional[str] = None):
        self.status = choices.MESSAGE_STATUS_FAILED
        self.sent_date = utils.get_utc_now()
        if error is not None:
            self.memo = error
        self.save()

    def mark_as_cancelled(self, message: Optional[str] = None):
        self.status = choices.MESSAGE_STATUS_CANCELLED
        if message is not None:
            self.memo = message
        self.save()

    def mark_as_skipped(self, message: Optional[str] = None):
        self.status = choices.MESSAGE_STATUS_SKIPPED
        if message is not None:
            self.memo = message
        self.save()
