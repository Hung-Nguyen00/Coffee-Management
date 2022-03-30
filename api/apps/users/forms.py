from __future__ import absolute_import, unicode_literals

import datetime

from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserChangeForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError

from apps.core.utils import random_with_n_digits
from apps.users.exceptions import PasswordsNotMatchException, PasswordValidateError
from apps.users.models import ResetPasswordOTP, User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class CustomPasswordResetForm(PasswordResetForm):
    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=None,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            otp = random_with_n_digits(6)
            ResetPasswordOTP.objects.filter(user=user).delete()
            ResetPasswordOTP.objects.create(user=user, otp=otp)

            context = {
                "email": email,
                "domain": domain,
                "site_name": site_name,
                "user": user,
                "otp": otp,
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                email,
                html_email_template_name=html_email_template_name,
            )


class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise PasswordsNotMatchException()
        try:
            password_validation.validate_password(password2, self.user)
        except ValidationError as error:
            raise PasswordValidateError(error.messages[0])
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        otp = self.data["otp"]

        self.user.set_password(password)
        reset_password_otp = ResetPasswordOTP.objects.get(otp=otp, user=self.user, is_verified=False)
        reset_password_otp.is_verified = True
        reset_password_otp.verified_at = datetime.datetime.now()

        if commit:
            self.user.save()
            reset_password_otp.save()
        return self.user
