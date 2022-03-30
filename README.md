

# APIs

## Prerequisites
- Python 3.6 or 3.7 (Ignore if using Docker)
- Virtualenv (Ignore if using Docker)
- Postgres 9.6 + (Ignore if using Docker)
- Redis (Ignore if using Docker)
- Docker (Optional)
- Docker Compose (Optional)

## Setup Configuration Files

```bash
# Edit DATABASE_URL in ./config/settings/.env
DATABASE_URL=postgres://goldfish:123456@postgres:5432/goldfish
```

## Install Pre-commit Hooks
Pre-commit hooks are executed as soon as you commit code to reformat and validate PEP8 standard

```bash
pre-commit install

# Test hooks
pre-commit run --all-files
```


## virtualenv

```bash
# 1. Create virtual env
cd api
python3 -m venv virtualenv
. virtualenv/bin/activate

# 2. Install dependency
pip install -r requirements/local.txt

# 3. Migrate database
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py seed_categories
$ ./manage.py seed_skills
$ ./manage.py sync_roles
$ ./manage.py seed_employees number_employee #please change number_employee to number, at least 100 in order to create fake project members.
$ ./manage.py seed_projects
$ ./manage.py seed_employee_timesheets

# 4. Generate JWT private/public key
openssl genrsa -out jwt_api_key 1024
openssl rsa -in jwt_api_key -pubout -out jwt_api_key.pub

# 5. Start Django
$ ./manage.py runserver 0.0.0.0:8000
```

## Health check
```bash
To show main page of django-health-check library (html) use:

http://localhost:8000/ht/status/
```
```bash
To show checks status in json format use:

http://localhost:8000/ht/status?format=json
```
```bash
To show status of one check named 'mycheck' in json format use:

http://myserver/status?format=json&checks=mycheck

These name check is available: db','cache', 'celery','storage'
```
```bash
To show status of some checks (mycheck1 and mycheck2) in json format use:

http://myserver/status?format=json&checks=mycheck1,mycheck2
```
```
HTTP status code:

200: If all queried checks are in status OK.
500: If any queried check is WRONG.
```

### Coverage
```bash
source  ./virtualenv/bin/activate
coverage run --source=apps manage.py test apps
```

## Django Admin
- URL: http://localhost/admin

## Swagger Document
- URL: http://localhost/docs

## Create new App

```bash
# 1. SSH to API Container
$ docker-compose exec api bash

# 2. Create new app folder
$ mkdir -p apps/[APP_NAME]

# 3. Create new app
$ ./manage.py startapp [APP_NAME] apps/[APP_NAME]

# 4. Update your app name in app config in app/[APP_NAME]/apps.py

name = 'apps.[APP_NAME]'
```

## Install new app

```python
# 5. Add new app in config/settings/common
LOCAL_APPS = (
    'apps.core.apps.CoreConfig',
    'apps.users.apps.UserConfig',
    'apps.APP_NAME',
)

```
## Best Practices
- separate into multiple small apps
- Avoid cycle dependency
- Should use UUID for Primary Key

Example

```python
import uuid

from django.db import models

user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```
