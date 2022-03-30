import phonenumbers
from django.conf import settings


def check_phone_number(phone: str) -> bool:
    try:
        if settings.VALIDATE_PHONE_NUMBER:
            if phone[0] != "+":
                phone = "+" + phone.strip()
            phone_validator = phonenumbers.parse(phone, None)
            return phonenumbers.is_possible_number(phone_validator)
    except Exception as ex:
        print(str(ex))
        return False
    return True
