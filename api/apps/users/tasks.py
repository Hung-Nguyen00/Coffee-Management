from apps.core.celery import app
from apps.uploads.services.usercases import UploadFileService
from apps.users.models import User
from apps.users.settings import app_settings


@app.task(autoretry_for=(Exception,))
def create_thumbnail_task(user_id: str, **kwargs):
    user = User.objects.filter(pk=user_id).first()
    if not user.avatar:
        return
    file_path = user.avatar
    service = UploadFileService(user)
    size = (
        app_settings.THUMBNAIL_FILE_HEIGHT,
        app_settings.THUMBNAIL_FILE_WIDTH,
    )
    name_suffix = "x".join(map(str, size))
    thumbnail_path = service.create_thumbnail(file_path, size)
    # user.update(avatar_thumb=thumbnail_path.get(name_suffix))
    user.avatar_thumb = thumbnail_path.get(name_suffix)
    user.save()


def send_create_oscar_user(user):
    app.send_task("create_oscar_user_map", [user])
