from typing import Dict, List

from django.contrib.auth.models import Group, Permission
from rolepermissions.permissions import available_perm_names
from rolepermissions.roles import assign_role
from rolepermissions.roles import get_user_roles as get_lib_roles
from rolepermissions.roles import remove_role
from rolepermissions.utils import camelToSnake

from apps.uploads.services.usercases import UploadFileService
from apps.users.api import serializers
from apps.users.exceptions import MissedUsernameOrEmailException, RoleDoesNotExist, UserNotExistsException
from apps.users.models import User
from apps.users.signals import user_avatar_updated_signal


def exists_user(username=None, email=None):
    if not username and not email:
        raise MissedUsernameOrEmailException()
    if username:
        queryset = User.objects.filter(username__iexact=username)
    else:
        queryset = User.objects.filter(email__iexact=email)
    count = queryset.count()
    return count > 0


def get_user(user_id: str) -> User:
    try:
        return User.objects.get(pk=user_id)
    except Exception:
        raise UserNotExistsException()


def update_user(instance: User, data: Dict, avatar: str):
    instance.email = data.get("email", instance.email)
    instance.first_name = data.get("first_name", instance.first_name)
    instance.last_name = data.get("last_name", instance.last_name)
    instance.phone = data.get("phone", instance.phone)
    instance.display_name = data.get("display_name", instance.display_name)
    instance.bio = data.get("bio", instance.bio)
    instance.enabled_2fa = data.get("enabled_2fa", instance.enabled_2fa)
    instance.is_active = data.get("is_active", instance.is_active)
    if "password" in data:
        password = data.get("password", instance.password)
        instance.set_password(password)
    if avatar != instance.avatar:
        service = UploadFileService(instance)
        if instance.avatar:
            service.delete(instance.avatar)
        instance.avatar_thumb = None
        instance.avatar = avatar
        instance.save()
        service.mark_file_used(avatar)
        user_avatar_updated_signal.send(sender=User, user=instance)
    instance.save()
    return instance


def handle_avatar_when_sign_up(avatar: str):
    if avatar:
        services = UploadFileService(None)
        services.mark_file_used(avatar)


def get_user_roles(user: User):
    lib_roles = get_lib_roles(user)
    roles_names = [r.get_name() for r in lib_roles]
    roles = Group.objects.filter(name__in=roles_names)
    serializer = serializers.RolesSerializer(roles, many=True)
    return serializer.data


def get_user_permissions(user: User):
    available_permissions = available_perm_names(user)
    permissions = Permission.objects.filter(codename__in=available_permissions)
    serializer = serializers.PermissionsSerializer(permissions, many=True)
    return serializer.data


def assign_user_role(user: User, role_name: str):
    try:
        assign_role(user, role_name)
    except Exception:
        raise RoleDoesNotExist()
    role = Group.objects.get(name=role_name)
    serializer = serializers.RolesSerializer(role)
    return serializer.data


def remove_user_role(user: User, role_name: str):
    try:
        remove_role(user, role_name)
    except Exception:
        raise RoleDoesNotExist()


def update_user_role(user: User, role_update: str = None, current_roles: List = None):
    if role_update:
        role_name = camelToSnake(role_update.replace(" ", ""))
        if current_roles and role_name not in current_roles:
            for role in current_roles:
                remove_role(user, role)
            assign_user_role(user=user, role_name=role_name)
        assign_user_role(user=user, role_name=role_name)
    elif current_roles:
        for role in current_roles:
            remove_role(user, role)
