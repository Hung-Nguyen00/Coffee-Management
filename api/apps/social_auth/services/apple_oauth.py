from datetime import timedelta

import jwt
import requests
from allauth.utils import generate_unique_username
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.social_auth.exceptions import LogInException
from apps.social_auth.models import AppleAccount, AppleApp
from apps.users.models import User


class AppleOAuth2:
    """apple authentication backend"""

    name = "apple"
    ACCESS_TOKEN_URL = "https://appleid.apple.com/auth/token"
    SCOPE_SEPARATOR = ","
    ID_KEY = "uid"

    def __init__(self):
        apple_app = AppleApp.objects.get(app="APPLE")
        self.apple_id_client = apple_app.apple_id_client
        self.apple_private_key = apple_app.apple_private_key
        self.apple_id_team = apple_app.apple_id_team
        self.apple_id_key = apple_app.apple_id_key

    def do_auth(self, data: dict):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        response_data = {}
        client_id, client_secret = self.get_key_and_secret()
        code = data.get("code", "")
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://example-app.com/redirect",
        }

        res = requests.post(AppleOAuth2.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get("id_token", None)
        if id_token:
            decoded = jwt.decode(id_token, "", verify=False)
            response_data.update({"email": decoded["email"]}) if "email" in decoded else None
            response_data.update({"uid": decoded["sub"]}) if "sub" in decoded else None
            apple_account = self.create_apple_account(decoded["email"], decoded["sub"])
            if apple_account.user:
                user = apple_account.user
            else:
                user = self.create_user(apple_account.email)
                apple_account.user = user
                apple_account.save()
            response = self.get_response_data(user)
            return response
        raise LogInException()

    def get_key_and_secret(self):
        headers = {"kid": self.apple_id_key}

        payload = {
            "iss": self.apple_id_team,
            "iat": timezone.now(),
            "exp": timezone.now() + timedelta(days=180),
            "aud": "https://appleid.apple.com",
            "sub": self.apple_id_client,
        }

        client_secret = jwt.encode(payload, self.apple_private_key, algorithm="ES256", headers=headers).decode("utf-8")

        return self.apple_id_client, client_secret

    @classmethod
    def create_apple_account(cls, email: str, apple_id: str) -> AppleAccount:
        try:
            apple_account = AppleAccount.objects.get(apple_id=apple_id)
        except AppleAccount.DoesNotExist:
            apple_account = AppleAccount.objects.create(
                email=email,
                apple_id=apple_id,
            )
        return apple_account

    @classmethod
    def create_user(cls, email: str) -> User:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            password = make_password(None)
            user = User.objects.create(
                email=email,
                password=password,
                username=generate_unique_username(txts=[email, "user"]),
            )
        return user

    @classmethod
    def get_response_data(cls, user: User) -> dict:
        enabled_2fa = user.enabled_2fa
        serializer_class = TokenObtainPairSerializer()
        serializer = serializer_class.get_token(user)
        access = serializer.access_token
        data = {
            "refresh": str(serializer),
            "access": str(access),
            "enabled_2fa": enabled_2fa,
        }

        return data
