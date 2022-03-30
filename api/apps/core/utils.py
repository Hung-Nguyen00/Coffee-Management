# type: ignore
import logging
import os
import random
import re
import string
import time
from datetime import datetime
from itertools import chain
from logging import Logger
from os import path
from random import randint
from typing import Optional

import boto3
import pytz
from django.conf import settings
from ipware.ip import get_client_ip

logger = logging.getLogger(__name__)


def get_logger(name: Optional[str] = "django") -> Logger:
    return logging.getLogger(name)


def get_now() -> datetime:
    return datetime.now(tz=pytz.utc)


def get_utc_now() -> datetime:
    """
    Get current UTC time
    :return:
    """
    return get_now().replace(tzinfo=pytz.utc)


def generate_password(password_length=20) -> str:
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz23456789!@#$"
    return "".join(random.choice(chars) for i in range(password_length))


def is_number(s: Optional[str]) -> bool:
    try:
        if s is None:
            return False
        float(str(s))  # for int, long and float
    except ValueError:
        return False
    return True


def is_production() -> bool:
    return settings.ENVIRONMENT == "production"


def get_app_version(request) -> Optional[str]:
    if not request or not hasattr(request, "META") or not isinstance(request.META, dict):
        return None
    return request.META.get("HTTP_APP_VERSION")


def get_device_id(request) -> Optional[str]:
    if not request or not hasattr(request, "META") or not isinstance(request.META, dict):
        return None
    return request.META.get("HTTP_DEVICE_ID")


def get_platform(request):
    try:
        if request.user_agent.os.family == "iOS":
            return "IOS"
        if request.user_agent.os.family == "Android":
            return "DROID"

        return "OTHER"
    except Exception as e:
        logger.warning(e)

    return None


def get_platform_version(request):
    try:
        return request.user_agent.os.version_string
    except Exception as e:
        logger.warning(e)

    return None


def get_ip_address(request) -> str:
    return get_client_ip(request)


def is_absolute_url(url: str) -> bool:
    if re.match(r"^https?://", url):
        return True
    return False


def get_static_url(file_path: str) -> str:
    if is_absolute_url(file_path):
        return file_path
    url = f"{settings.STATIC_URL}{file_path}"
    return get_absolute_url(url)


def get_media_url(file_path: str) -> str:
    if is_absolute_url(file_path):
        return file_path
    url = f"{settings.MEDIA_URL}{file_path}"
    return get_absolute_url(url)


def get_absolute_url(url: str) -> str:
    if is_absolute_url(url):
        return url

    base_url = str(settings.BASE_URL).rstrip("/")
    return f'{base_url}/{url.lstrip("/")}'


def get_storage_path(filename: str, folder_name: str) -> str:
    now = datetime.now()
    folder = "/".join([folder_name, str(now.year), f"{now:%m}", f"{now:%d}"])
    path_url = [folder, path.basename(filename)]
    return path.join(*path_url)


def generate_pre_signed_url_for_s3(file_name: str, file_type: str):
    bucket_name = settings.AWS_LOCATION
    s3 = boto3.client("s3")
    pre_signed_post = s3.generate_presigned_post(
        Bucket=bucket_name,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[{"acl": "public-read"}, {"Content-Type": file_type}],
        ExpiresIn=settings.S3_PRE_SIGNED_POST_URL_EXPIRES,
    )
    return pre_signed_post


def random_with_n_digits(n, is_testing=None):
    if is_testing:
        return settings.TESTING_RESET_PASSWORD_OTP
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def is_reset_password_otp_expired(created_time) -> bool:
    return (int(time.time()) - created_time.timestamp()) > settings.RESET_PASSWORD_OTP_EXPIRE_TIME


def random_string():
    chars_fixed = string.ascii_letters + string.digits
    min_size_pass = 8
    max_size_pass = 16
    username = "".join(random.choice(chars_fixed) for x in range(random.randint(min_size_pass, max_size_pass)))
    return username


def fake_email(prefix: str = None) -> str:
    if not prefix:
        prefix = random_string().lower()
    return prefix + settings.FAKE_EMAIL_FORMAT


def check_fake_email(email: str) -> bool:
    return True if settings.FAKE_EMAIL_FORMAT in email else False


def get_request_from_inspect_stack():
    import inspect

    for frame_record in reversed(inspect.stack()):
        if frame_record[3] == "get_response":
            request = frame_record[0].f_locals["request"]
            break
        else:
            request = None
    return request


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


def extra_args(**kwargs):
    extra_args = kwargs
    """
    Add extra arguments when connect a signal ex:
    """

    def inner1(f, **kwargs):
        def inner2(sender, instance, **kwargs):
            f(sender, instance, **extra_args, **kwargs)

        return inner2

    return inner1


def mkdir(file_path: str) -> str:
    os.makedirs(file_path, exist_ok=True)
    return file_path


def mkdir_with_current_date(file_path: str) -> str:
    d = time.strftime("%Y/%m/%d")
    p = f"{file_path}/{d}"
    mkdir(p)
    return p
