from django.contrib.auth.models import Group, Permission
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import PasswordChangeSerializer, PasswordResetSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rolepermissions.roles import get_user_roles as get_role_list
from rolepermissions.roles import retrieve_role

from apps.core.utils import check_fake_email
from apps.users.exceptions import PasswordResetOTPException
from apps.users.forms import CustomPasswordResetForm, CustomSetPasswordForm
from apps.users.models import ResetPasswordOTP, User
from apps.users.services import get_user, get_user_roles, update_user, update_user_role
from apps.users.signals import user_signup_signal
from apps.users.validators import EmailValidator, PasswordValidator, PhoneValidator, ResetPasswordOTPValidator


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField("get_user_role")

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "bio",
            "display_name",
            "enabled_2fa",
            "role",
            "is_active",
        )
        extra_kwargs = {"password": {"write_only": True}}
        validators = [UniqueTogetherValidator(queryset=User.objects.all(), fields=["username"])]

    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        allow_null=False,
        validators=[EmailValidator(), UniqueValidator(queryset=User.objects.all(), lookup="iexact")],
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=False,
        validators=[PhoneValidator(), UniqueValidator(queryset=User.objects.all())],
    )

    @classmethod
    def get_avatar(cls, obj):
        return obj.get_avatar()

    @classmethod
    def get_user_role(cls, obj):
        return get_user_roles(obj)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["email"] = instance.email if not check_fake_email(instance.email) else None
        return ret

    def update(self, instance: User, validated_data):
        avatar = self.initial_data.get("avatar", instance.avatar)
        role_update = self.initial_data.get("role")
        current_roles = [r.get_name() for r in get_role_list(instance)]
        update_user_role(user=instance, role_update=role_update, current_roles=current_roles)
        instance = update_user(instance, validated_data, avatar)
        return instance


class UserRegisterSerializer(RegisterSerializer):
    avatar = serializers.CharField(max_length=1000, required=False, default="")
    username = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.all(), lookup="iexact")],
    )
    email = serializers.EmailField(required=True, allow_null=False, validators=[EmailValidator()])
    first_name = serializers.CharField(max_length=30, required=False, default="")
    last_name = serializers.CharField(max_length=150, required=False, default="")
    phone = serializers.CharField(
        max_length=30,
        required=False,
        default="",
        validators=[PhoneValidator()],
    )
    bio = serializers.CharField(max_length=1000, required=False, default="")
    display_name = serializers.CharField(max_length=100, required=False, default="")
    password1 = serializers.CharField(write_only=True, validators=[PasswordValidator()])

    def custom_signup(self, request, user):
        user.avatar = self.validated_data.get("avatar", None)
        user.phone = self.validated_data.get("phone", "")
        user.display_name = self.validated_data.get("display_name", "")
        user.bio = self.validated_data.get("bio", "")
        user.save()

        user_signup_signal.send(sender=User, user=user)


class UserPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = CustomPasswordResetForm


class UserPasswordChangeSerializer(PasswordChangeSerializer):
    old_password = serializers.CharField(max_length=128, allow_blank=True)
    new_password1 = serializers.CharField(
        max_length=128, allow_blank=True, validators=[PasswordValidator(old_password)]
    )
    new_password2 = serializers.CharField(max_length=128, allow_blank=True)


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    otp = serializers.CharField(max_length=6, validators=[ResetPasswordOTPValidator()])

    set_password_form_class = CustomSetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        otp = attrs.get("otp")

        reset_password_otp = ResetPasswordOTP.objects.filter(otp=otp, is_verified=False).first()

        user = User.objects.get(pk=reset_password_otp.user.pk)
        self._errors = {}
        self.custom_validation(attrs)
        self.set_password_form = self.set_password_form_class(user=user, data=attrs)

        if not self.set_password_form.is_valid():
            if self.set_password_form.errors and self.set_password_form.errors.values():
                raise PasswordResetOTPException(list(self.set_password_form.errors.values())[0])

        return attrs

    def save(self):
        return self.set_password_form.save()


class UserTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        # check exist user
        user_id = refresh.payload.get("id", None)
        user = get_user(user_id=user_id)

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)
            data["enabled_2fa"] = user.enabled_2fa

        return data


class ResponseTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    enabled_2fa = serializers.BooleanField(read_only=True)


class UserLoginBodySerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ResendConfirmBodySerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class RolesSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "role",
            "description",
        )

    def get_role(self, obj):
        return retrieve_role(obj.name).role

    def get_description(self, obj):
        return retrieve_role(obj.name).description
