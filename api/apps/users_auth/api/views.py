from allauth.account.views import ConfirmEmailView
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.serializers import (
    ResendConfirmBodySerializer,
    ResponseTokenSerializer,
    UserLoginBodySerializer,
    UserSerializer,
    UserTokenRefreshSerializer,
)
from apps.users_auth.services import resend_confirmation_email


class CustomRegisterView(RegisterView):
    def get_response_data(self, user):
        if settings.ACCOUNT_EMAIL_VERIFICATION == settings.ACCOUNT_EMAIL_VERIFICATION_MANDATORY:
            return {"detail": _("Verification e-mail sent.")}
        return UserSerializer(user).data


class CustomLoginView(LoginView):
    def get_response(self):
        enabled_2fa = self.user.enabled_2fa
        serializer_class = TokenObtainPairSerializer()
        serializer = serializer_class.get_token(self.user)
        access = serializer.access_token
        data = {
            "refresh": str(serializer),
            "access": str(access),
            "enabled_2fa": enabled_2fa,
        }
        return Response(ResponseTokenSerializer(data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserLoginBodySerializer,
        responses={200: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = UserTokenRefreshSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomConfirmEmailView(ConfirmEmailView):
    allowed_methods = ("GET",)

    def get(self, request, *args, **kwargs):
        try:
            confirmation = self.get_object()
        except Exception:
            raise Http404()
        confirmation.confirm(self.request)
        return HttpResponseRedirect(redirect_to=settings.SIGNUP_REDIRECT_URL)


class ResendConfirmEmailView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ResendConfirmBodySerializer)
    def post(self, request):
        email = request.data["email"]
        resend_confirmation_email(email)
        return Response({"detail": _("Verification e-mail sent.")}, status=status.HTTP_200_OK)
