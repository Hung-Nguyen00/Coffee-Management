from django.urls import include, path

urlpatterns = [
    path("users/", include("apps.users.api.urls")),
    path("", include("apps.users_auth.api.urls")),
    path("social-auth/", include("apps.social_auth.api.urls")),
    path("uploads/", include("apps.uploads.api.urls")),
    path("otp/", include("apps.otp_auth.api.urls"))
]
