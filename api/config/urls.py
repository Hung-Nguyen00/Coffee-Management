import os
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="App API",
        default_version="v1",
        description="App API",
        contact=openapi.Contact(email="noreply@goldfishcode.com"),
        license=openapi.License(name="API License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=os.environ.get("BASE_URL"),
)


urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("v1/", include("config.api")),
]
