from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_role


class IsAdminSuperUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_admin = has_role(user, "admin")
        is_super_user = bool(user.is_staff and user.is_superuser)
        return is_super_user or is_admin
