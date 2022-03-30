import django.contrib.auth.password_validation as password_validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as validate_email_core
from rest_framework.serializers import ValidationError as DRFValidationError

from apps.core.utils import is_reset_password_otp_expired
from apps.core.validation import check_phone_number
from apps.users.models import ResetPasswordOTP, User


class PhoneValidator(object):
    def __call__(self, phone):
        if not check_phone_number(phone):
            raise DRFValidationError("This phone is invalid.", code=2015)

        # if User.objects.filter(phone=phone).exists():
        #     raise DRFValidationError("This phone is already registered with another user.", code=2014)


class EmailValidator(object):
    def __call__(self, email):
        if email.strip() == "":
            raise DRFValidationError("Email is required.", code=2000)

        try:
            validate_email_core(email)
        except ValidationError as error:
            raise DRFValidationError(error.messages[0], code=2007)

        # if User.objects.filter(email__iexact=email.lower()).exists():
        #     raise DRFValidationError("A user is already registered with this e-mail address.", code=2004)


class PasswordValidator(object):
    def __init__(self, old_password=None):
        self.old_password = old_password

    def __call__(self, password):
        try:
            password_validators.validate_password(password)
        except ValidationError as error:
            raise DRFValidationError(error.messages[0], code=2006)

        if self.old_password and self.old_password == password:
            raise DRFValidationError("Old password and new password can not be the same", code=2010)


class ResetPasswordOTPValidator(object):
    def __call__(self, otp):
        reset_password_otp = ResetPasswordOTP.objects.filter(otp=otp, is_verified=False).first()
        if not reset_password_otp:
            raise DRFValidationError("This OTP code is invalid or verified.", code=2012)

        if is_reset_password_otp_expired(reset_password_otp.created):
            raise DRFValidationError("This OTP code is expired. Please request new code.", code=2013)
