from base64 import b32encode
from typing import Optional

from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.users.models import User


def get_user_totp_device(user: User, confirmed=None) -> Optional[TOTPDevice]:
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
    else:
        return None


def verify_otp(user: User, otp: str) -> bool:
    device = get_user_totp_device(user)
    if device is not None and device.verify_token(otp):
        if not device.confirmed:
            device.confirmed = True
            device.save()
            user.enabled_2fa = True
            user.save()
        return True
    return False


def disable_2fa(user: User):
    TOTPDevice.objects.filter(user=user).delete()
    user.enabled_2fa = False
    user.save()


def generate_qr(user: User) -> tuple:
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=False)
    url = device.config_url
    secret = b32encode(device.bin_key).decode("utf8")
    return url, secret
