from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import ResetPasswordOTP, User


class UserAdmin(AuthUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "enabled_2fa",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def has_add_permission(self, request):
        return True


admin.site.register(User, UserAdmin)


@admin.register(ResetPasswordOTP)
class ResetPasswordOTPAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = None

    list_display = ("user", "otp", "is_verified", "verified_at", "created")
    search_fields = ("user__username", "user__email")
    raw_id_fields = ("user",)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def has_add_permission(self, request):
        return False

    def get_ordering(self, request):
        return ["-created"]
