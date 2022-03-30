App Otp Auth
---

## Overview

This application is an implementation for two-factor authentication to Django using one-time passwords.


## Requirements
* django-otp==0.9.3

## Setup

Edit your `settings/common.py` file:

### Installed apps


```python

THIRD_PARTY_APPS = (
    # otp
    "django_otp",
    "django_otp.plugins.otp_totp",
)

LOCAL_APPS = (
    # ...
    "apps.otp_auth.apps.OtpConfig",
    # ...
)
```


### Rest Auth
```python
REST_AUTH_SERIALIZERS = {
    "TOKEN_SERIALIZER": "apps.otp_auth.serializers.TwoFactorTokenObtainPairSerializer",
}
```


### Rest Framework

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("apps.otp_auth.permissions.IsOtpVerified",)
}
```

## Endpoints
These endpoint for 2FA.

### Get qr code
```bash
POST /v1/otp/2fa/
```

### Enable 2fa
```bash
PATCH /v1/otp/2fa/
```

### Disable 2fa
```bash
DELETE /v1/otp/2fa/
```

### Verify otp
```bash
POST /v1/otp/2fa/login/
```
