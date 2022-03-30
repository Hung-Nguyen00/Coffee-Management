App Users Auth
---

## Overview

This application is an implementation of User Authentication with social account.


## Prerequisites
* Python 3.6
* Django >= 2.2.7
* django-oauth-toolkit==1.2.0
* django-cors-middleware==1.4.0
* django-rest-auth==0.9.5
* django-allauth==0.40.0
* cryptography==2.8

## Setup

Edit your `settings/common.py` file:

### Installed apps


```python

THIRD_PARTY_APPS = (
    # Auth
    'rest_framework.authtoken',
    'oauth2_provider',
    'rest_auth',

    # social auth
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # Registration
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
)

LOCAL_APPS = (
    # ...
    'apps.social_auth.apps.SocialAuthConfig',
    # ...
)
```

### Middleware

```python
MIDDLEWARE = [
    # ...
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]
```

### Config allauth module

https://django-allauth.readthedocs.io/en/latest/configuration.html

```python
SOCIALACCOUNT_CALLBACK_URL = 'http://localhost'
SOCIALACCOUNT_ADAPTER = 'app.social_auth.adapter.SocialAccountAdapter'

```

### Authentication backend

```python
AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',  # if Oauth2 is enabled
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend'
)
```
### Create Social applications facebook and google
- Go to facebook developer: https://developers.facebook.com/ create a new app and get "Client id" and "Secret key"
- Go to google console: https://code.google.com/apis/console create a new project,
 and then create credentials "Oauth client ID", "Client id" and "Secret key"
- Go to admin page create Social applications with provider "Facebook" and "Google" with "Client id" and "Secret key".
