import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from model_utils.managers import SoftDeletableManagerMixin
from model_utils.models import TimeStampedModel

from apps.core.utils import get_media_url, get_storage_path


class CustomUserManager(SoftDeletableManagerMixin, UserManager):
    pass


class User(AbstractUser):
    # objects = CustomUserManager(_emit_deprecation_warnings=True)
    objects = CustomUserManager()
    available_objects = CustomUserManager()
    all_objects = UserManager()

    class Meta:
        default_manager_name = "objects"
        ordering = ["-date_joined"]

    def avatar_path(self, filename, *args, **kwargs):
        return get_storage_path(filename, "avatar", str(self.pk))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    avatar = models.CharField(null=True, blank=True, max_length=1000)  # type: str
    avatar_thumb = models.CharField(null=True, blank=True, max_length=1000)  # type: str
    phone = models.CharField(default="", blank=True, max_length=30)
    bio = models.CharField(default="", blank=True, max_length=1000)
    display_name = models.CharField(default="", blank=True, max_length=100)
    enabled_2fa = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def name(self):
        name = "%s %s" % (self.first_name, self.last_name)
        if not name.strip():
            name = self.username
        return name

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        return self.name

    def get_first_name(self):
        if self.first_name_name:
            return self.first_name_name
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and not self.username:
            from allauth.utils import generate_unique_username

            self.username = generate_unique_username(
                [self.first_name, self.last_name, self.email, self.username, "user"]
            )

        self.first_name = " ".join(self.first_name.split())
        self.last_name = " ".join(self.last_name.split())

        return super().save(*args, **kwargs)

    def get_avatar(self):
        if self.avatar_thumb:
            return get_media_url(self.avatar_thumb)
        elif self.avatar:
            return get_media_url(self.avatar)
        else:
            return None

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)


class ResetPasswordOTP(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["user", "is_verified"]),
        ]
        verbose_name = "Reset Password OTP"
        verbose_name_plural = "Reset Password OTPs"

    def __str__(self):
        return f"{self.created}: {self.user} - {self.otp}"
