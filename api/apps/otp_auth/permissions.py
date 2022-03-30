import jwt
from django_otp import user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.permissions import IsAuthenticated


class IsOtpVerified(IsAuthenticated):
    def has_permission(self, request, view):
        is_allowed = super().has_permission(request, view)
        if not is_allowed or not request.user.enabled_2fa:
            return is_allowed

        if user_has_device(request.user):
            return self.otp_is_verified(request)

        return False

    @classmethod
    def otp_is_verified(cls, request) -> bool:
        token = str(request.headers.get("Authorization")).split("Bearer ")[1]
        payload = jwt.decode(token, verify=False)
        two_fa_device_id = payload.get("2fa_device_id")

        if two_fa_device_id:
            device = TOTPDevice.objects.filter(id=two_fa_device_id).first()
            if device and device.user_id != request.user.pk:
                return False
            else:
                return True
        else:
            return False
