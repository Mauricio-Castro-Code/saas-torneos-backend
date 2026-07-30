from rest_framework.permissions import BasePermission

from accounts.models import Usuario

from .models import Equipo


class EsJugador(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Usuario.Role.JUGADOR
        )


class EsCapitanDeSuEquipo(BasePermission):
    """Valida pertenencia (capitan_id == request.user.id), no solo el rol."""

    def has_object_permission(self, request, view, obj):
        equipo = obj if isinstance(obj, Equipo) else obj.equipo
        return equipo.capitan_id == request.user.id
