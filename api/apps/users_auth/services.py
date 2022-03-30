from allauth.account.models import EmailAddress, EmailConfirmation
from rest_framework.validators import ValidationError

from apps.users.models import User


def resend_confirmation_email(email: str):
    user = User.objects.filter(email=email).first()
    if not user:
        raise ValidationError("There is not user exist with this email.")
    email_address = EmailAddress.objects.filter(user=user, email=user.email).first()

    # Delete expired token
    EmailConfirmation.objects.delete_expired_confirmations()
    qs = EmailConfirmation.objects.all_valid().filter(email_address=email_address)
    if not qs.exists():
        email_confirmation = EmailConfirmation.create(email_address=email_address)
    else:
        email_confirmation = qs.first()

    # Send
    email_confirmation.send(signup=True)
