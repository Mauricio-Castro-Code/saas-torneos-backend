from rest_framework.permissions import BasePermission

from accounts.models import Usuario


class EsJugador(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Usuario.Role.JUGADOR
        )
