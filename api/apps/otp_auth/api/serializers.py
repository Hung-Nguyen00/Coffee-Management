from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TwoFactorTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        device: TOTPDevice = TOTPDevice.objects.filter(user=user).first()
        if device and user.enabled_2fa:
            token["2fa_device_id"] = str(device.id)
        else:
            token["2fa_device_id"] = None
        return token


class TOTPBodySerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)


class QRCodeSerializer(serializers.Serializer):
    qr = serializers.CharField(read_only=True)
    secret = serializers.CharField(read_only=True)


class TwoFaResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    enabled_2fa = serializers.BooleanField(read_only=True)
