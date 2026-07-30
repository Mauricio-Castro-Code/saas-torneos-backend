from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import Usuario
from leagues.permissions import EsAdmin
from teams.models import Jugador

from .models import Categoria, Jornada, Partido, Temporada
from .permissions import EsAdminOSoloLectura
from .serializers import (
    CategoriaSerializer,
    JornadaSerializer,
    PartidoSerializer,
    TemporadaSerializer,
)


class TemporadaViewSet(viewsets.ModelViewSet):
    serializer_class = TemporadaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Temporada.objects.filter(liga__admin=self.request.user)


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Categoria.objects.filter(temporada__liga__admin=self.request.user)


def _liga_id_del_jugador(user):
    """ID de la liga del equipo del jugador autenticado, o None si no tiene equipo."""
    jugador = Jugador.objects.filter(usuario=user).select_related(
        "equipo__categoria__temporada__liga"
    ).first()
    return jugador.equipo.categoria.temporada.liga_id if jugador else None


class JornadaViewSet(viewsets.ModelViewSet):
    serializer_class = JornadaSerializer
    permission_classes = [EsAdminOSoloLectura]

    def get_queryset(self):
        user = self.request.user
        if user.role == Usuario.Role.ADMIN:
            return Jornada.objects.filter(categoria__temporada__liga__admin=user)
        liga_id = _liga_id_del_jugador(user)
        if liga_id is None:
            return Jornada.objects.none()
        return Jornada.objects.filter(categoria__temporada__liga_id=liga_id)


class PartidoViewSet(viewsets.ModelViewSet):
    """CRUD de partidos, incluida la captura de resultado (goles_local/goles_visitante)
    vía PATCH — deliberadamente sin action aparte, para que capturar un resultado
    sea un solo request con pocos clics desde el front.

    Lectura abierta a cualquier jugador autenticado (solo ve los partidos de la
    liga de su propio equipo); escritura solo admin, ver EsAdminOSoloLectura."""

    serializer_class = PartidoSerializer
    permission_classes = [EsAdminOSoloLectura]

    def get_queryset(self):
        user = self.request.user
        if user.role == Usuario.Role.ADMIN:
            return Partido.objects.filter(
                jornada__categoria__temporada__liga__admin=user
            )
        liga_id = _liga_id_del_jugador(user)
        if liga_id is None:
            return Partido.objects.none()
        return Partido.objects.filter(
            jornada__categoria__temporada__liga_id=liga_id
        )
