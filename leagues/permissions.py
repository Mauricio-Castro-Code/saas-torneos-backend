from rest_framework.permissions import BasePermission

from accounts.models import Usuario


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Usuario.Role.ADMIN
        )
