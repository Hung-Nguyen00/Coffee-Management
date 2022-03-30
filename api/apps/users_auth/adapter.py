from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from apps.core.helpers.branchio import generate_branch_io_link


class AccountAdapter(DefaultAccountAdapter):
    def respond_email_verification_sent(self, request, user):
        """
        We don't need this redirect.
        """
        pass

    def get_email_confirmation_url(self, request, emailconfirmation, **kwargs):
        slug = "v1/account/activate"
        if "slug" in kwargs:
            slug = kwargs.get("slug")
        return "{}/{}/{}".format(settings.BASE_URL.rstrip("/"), slug, emailconfirmation.key)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        if settings.USE_BRANCH_IO:
            activate_url = generate_branch_io_link(
                {"action": "verify", "key": emailconfirmation.key, "email": emailconfirmation.email_address.email}
            )
        else:
            activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "expire_day": settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
            "frontend_url": settings.FRONTEND_BASE_URL,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
