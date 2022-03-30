from apps.otp_auth.api import views
from django.urls import path

urlpatterns = [
    path(
        "2fa/",
        views.TwoFaCreateRetrieveUpdateDeleteView.as_view(
            {
                "post": "create",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="2fa",
    ),
    path(
        "2fa/login/",
        views.TwoFaVerifyView.as_view(),
        name="2fa-login",
    ),
]
