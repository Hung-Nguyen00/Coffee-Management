from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.helpers import _add_social_account
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.core.utils import fake_email
from apps.social_auth import exceptions


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Validate white list domain
        domain_list = settings.GOOGLE_LOGIN_DOMAINS
        if domain_list:
            email_domain = (sociallogin.user.email).split("@")[1]
            if email_domain not in domain_list:
                raise exceptions.SocialDomainInvalidException()
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return
        # check required email
        if not sociallogin.account.extra_data.get("email", None):
            sociallogin.user.email = fake_email(str(sociallogin.account.extra_data["id"]))
            email_address = EmailAddress(email=sociallogin.user.email)
            sociallogin.email_addresses.append(email_address)
            return
        user = self.find_user(sociallogin)
        if user:
            sociallogin.user = user
        if sociallogin.account.provider in ["twitter"]:
            self.save_user(request, sociallogin)

    @classmethod
    def find_user(cls, sociallogin):
        return get_user_model().objects.filter(email__iexact=sociallogin.user.email).first()

    def save_user(self, request, sociallogin, form=None):
        user = self.find_user(sociallogin)
        social_account = sociallogin.account
        if not user:
            user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form=None)
            user.is_social = True
            sociallogin.created = True
            user.save()
        else:
            request.user = user
            _add_social_account(request, sociallogin)
        # save avatar
        avatar = social_account.get_avatar_url()
        if avatar:
            user.avatar = avatar
        user.save()
        return user
