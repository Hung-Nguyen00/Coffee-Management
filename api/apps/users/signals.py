from django.dispatch import Signal

user_signup_signal = Signal(providing_args=["user"])
user_avatar_updated_signal = Signal(providing_args=["user"])
