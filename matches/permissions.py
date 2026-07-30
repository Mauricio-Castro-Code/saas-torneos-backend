from rest_framework.permissions import SAFE_METHODS, BasePermission

from accounts.models import Usuario


class EsAdminOSoloLectura(BasePermission):
    """Cualquier usuario autenticado puede leer (jornadas/horarios son
    consulta habitual de jugadores); solo el admin puede escribir."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == Usuario.Role.ADMIN
