from django.urls import path
from rest_auth.registration.views import SocialAccountListView

from apps.social_auth.api.views import (
    AppleLoginView,
    FacebookLoginView,
    GoogleLoginView,
    LinkedinLoginView,
    TwitterAuthorizationCallBackView,
    TwitterAuthorizationView,
    TwitterLoginView,
)

urlpatterns = [
    path("facebook/", FacebookLoginView.as_view(), name="fb_login"),
    path("twitter/authorization/", TwitterAuthorizationView.as_view(), name="twitter_authorization"),
    path("twitter/callback/", TwitterAuthorizationCallBackView.as_view(), name="twitter_callback_view"),
    path("twitter/", TwitterLoginView.as_view(), name="twitter_login"),
    path("linkedin/", LinkedinLoginView.as_view(), name="linkedin_login"),
    path("google/", GoogleLoginView.as_view(), name="google_login"),
    path("apple/", AppleLoginView.as_view(), name="apple-login"),
    path("social-accounts/", SocialAccountListView.as_view(), name="socialaccount_connections"),
]
