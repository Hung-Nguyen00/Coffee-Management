from apps.otp_auth.api import serializers
from apps.otp_auth.api.serializers import TwoFactorTokenObtainPairSerializer
from apps.otp_auth.services import disable_2fa, generate_qr, verify_otp
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from apps.users.api.serializers import UserSerializer


class TwoFaResponse:
    def get_response(self):
        enabled_2fa = self.request.user.enabled_2fa
        serializer_class = TwoFactorTokenObtainPairSerializer
        serializer = serializer_class().get_token(self.request.user)
        access = serializer.access_token
        data = serializers.TwoFaResponseSerializer(
            {
                "refresh": str(serializer),
                "access": str(access),
                "enabled_2fa": enabled_2fa,
            }
        ).data
        return Response(data, status=status.HTTP_200_OK)


class TwoFaCreateRetrieveUpdateDeleteView(TwoFaResponse, viewsets.ModelViewSet):

    """
    Use this endpoint to set up a new TOTP device
    """

    serializer_class = UserSerializer

    @swagger_auto_schema(
        request_body=serializers.serializers.Serializer,
        responses={200: openapi.Response("response description", serializers.QRCodeSerializer)},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        url, secret = generate_qr(user=user)
        data = serializers.QRCodeSerializer({"qr": url, "secret": secret}).data
        return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: openapi.Response("response description", serializers.TwoFaResponseSerializer)})
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        disable_2fa(user=user)
        return self.get_response()

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        request_body=serializers.TOTPBodySerializer,
        responses={200: openapi.Response("response description", serializers.TwoFaResponseSerializer)},
    )
    def partial_update(self, request, *args, **kwargs):
        otp = self.request.data.get("otp")
        user = self.request.user
        if verify_otp(user=user, otp=otp):
            return self.get_response()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TwoFaVerifyView(TwoFaResponse, generics.CreateAPIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.TOTPBodySerializer,
        responses={200: openapi.Response("response description", serializers.TwoFaResponseSerializer)},
    )
    def post(self, request, *args, **kwargs):
        otp = self.request.data.get("otp")
        user = request.user
        if verify_otp(user=user, otp=otp):
            return self.get_response()
        return Response(status=status.HTTP_400_BAD_REQUEST)
