from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from leagues.permissions import EsAdmin

from .models import Categoria, Jornada, Partido, Temporada
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


class JornadaViewSet(viewsets.ModelViewSet):
    serializer_class = JornadaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Jornada.objects.filter(categoria__temporada__liga__admin=self.request.user)


class PartidoViewSet(viewsets.ModelViewSet):
    """CRUD de partidos, incluida la captura de resultado (goles_local/goles_visitante)
    vía PATCH — deliberadamente sin action aparte, para que capturar un resultado
    sea un solo request con pocos clics desde el front."""

    serializer_class = PartidoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Partido.objects.filter(
            jornada__categoria__temporada__liga__admin=self.request.user
        )
