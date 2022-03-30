from allauth.socialaccount.models import SocialAccount, SocialApp
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.signals import pre_social_login
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterConnectSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from twython import Twython

from apps.social_auth.api.serializers import AppleBodySerializer, SocialBodySerializer, SocialLoginSerializer
from apps.users.api.serializers import ResponseTokenSerializer


@receiver(pre_social_login)
def handle_duplicate_email(sender, request, sociallogin, **kwargs):
    if settings.ACCOUNT_EMAIL_VERIFICATION == "mandatory":
        data = sociallogin.serialize()
        account = data.get("user", None)
        if account:
            email = account.get("email", "")
            if email:  # if social account register by email
                try:
                    user = get_user_model().objects.get(email=email)
                    social_accounts = SocialAccount.objects.filter(provider=sociallogin.account.provider, user=user)
                    if not social_accounts.exists():
                        sociallogin.connect(request, user)
                except get_user_model().DoesNotExist:
                    return


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    serializer_class = SocialLoginSerializer

    @swagger_auto_schema(
        request_body=SocialBodySerializer,
        responses={200: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super(GoogleLoginView, self).post(request, *args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class().get_token(self.user)
        enabled_2fa = self.user.enabled_2fa
        data = {
            "refresh": str(serializer),
            "access": str(serializer.access_token),
            "enabled_2fa": enabled_2fa,
        }
        return Response(ResponseTokenSerializer(data).data, status=status.HTTP_200_OK)


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    serializer_class = SocialLoginSerializer

    @swagger_auto_schema(
        request_body=SocialBodySerializer,
        responses={200: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super(FacebookLoginView, self).post(request, *args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class().get_token(self.user)
        enabled_2fa = self.user.enabled_2fa
        data = {
            "refresh": str(serializer),
            "access": str(serializer.access_token),
            "enabled_2fa": enabled_2fa,
        }
        return Response(ResponseTokenSerializer(data).data, status=status.HTTP_200_OK)


class TwitterAuthorizationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        twitter_app = SocialApp.objects.filter(provider="twitter").first()
        if not twitter_app:
            return
        client_id = twitter_app.client_id
        client_secret = twitter_app.secret

        twitter = Twython(client_id, client_secret)
        twitter_url_callback = settings.BASE_URL + reverse("twitter_callback_view")
        # twitter_url_callback = 'http://ab5f7d22.ngrok.io' + reverse('twitter_callback_view')

        auth = twitter.get_authentication_tokens(callback_url=twitter_url_callback)

        url = auth["auth_url"]
        oauth_token = auth["oauth_token"]
        oauth_token_secret = auth["oauth_token_secret"]

        cache.set(oauth_token, oauth_token_secret)
        return Response({"url": url}, status=status.HTTP_200_OK)


class TwitterLoginView(SocialLoginView):
    permission_classes = (AllowAny,)
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter

    def post(self, request, *args, **kwargs):
        return super(TwitterLoginView, self).post(request, *args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class().get_token(self.user)
        enabled_2fa = self.user.enabled_2fa
        data = {
            "refresh": str(serializer),
            "access": str(serializer.access_token),
            "enabled_2fa": enabled_2fa,
        }
        return Response(ResponseTokenSerializer(data).data, status=status.HTTP_200_OK)


class TwitterAuthorizationCallBackView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        oauth_verifier = request.GET["oauth_verifier"]
        oauth_token = request.GET["oauth_token"]
        oauth_token_secrete = cache.get(oauth_token)

        twitter_app = SocialApp.objects.filter(provider="twitter").first()
        if not twitter_app:
            return
        client_id = twitter_app.client_id
        client_secret = twitter_app.secret

        twitter = Twython(client_id, client_secret, oauth_token, oauth_token_secrete)

        final_step = twitter.get_authorized_tokens(oauth_verifier)
        access_token = final_step["oauth_token"]
        access_token_secret = final_step["oauth_token_secret"]

        url_redirect = (
            settings.FRONTEND_BASE_URL
            + "/twitter"
            + "?access_token=%s&access_token_secret=%s" % (access_token, access_token_secret)
        )

        return HttpResponseRedirect(url_redirect)


class LinkedinLoginView(SocialLoginView):
    adapter_class = LinkedInOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    serializer_class = SocialLoginSerializer

    @swagger_auto_schema(
        request_body=SocialBodySerializer,
        responses={200: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super(LinkedinLoginView, self).post(request, *args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class().get_token(self.user)
        enabled_2fa = self.user.enabled_2fa
        data = {
            "refresh": str(serializer),
            "access": str(serializer.access_token),
            "enabled_2fa": enabled_2fa,
        }
        return Response(ResponseTokenSerializer(data).data, status=status.HTTP_200_OK)


class AppleLoginView(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    client_class = AppleOAuth2Client
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    serializer_class = SocialLoginSerializer

    @swagger_auto_schema(
        request_body=AppleBodySerializer,
        responses={200: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super(AppleLoginView, self).post(request, *args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class().get_token(self.user)
        enabled_2fa = self.user.enabled_2fa
        data = {
            "refresh": str(serializer),
            "access": str(serializer.access_token),
            "enabled_2fa": enabled_2fa,
        }
        return Response(ResponseTokenSerializer(data).data, status=status.HTTP_200_OK)
