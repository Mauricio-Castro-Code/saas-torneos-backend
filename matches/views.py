from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from leagues.permissions import EsAdmin

from .models import Categoria, Temporada
from .serializers import CategoriaSerializer, TemporadaSerializer


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
