from django.contrib import admin

from apps.social_auth.models import AppleAccount, AppleApp


@admin.register(AppleApp)
class AppleAppAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "app", "created", "modified")
    search_fields = ("name",)


@admin.register(AppleAccount)
class AppleAccountAdmin(admin.ModelAdmin):
    list_display = ("apple_id", "email", "user", "created", "modified")
    search_fields = (
        "apple_id",
        "email",
    )
    raw_id_fields = ("user",)
