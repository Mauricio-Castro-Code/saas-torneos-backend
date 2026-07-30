from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from leagues.permissions import EsAdmin

from .models import Equipo
from .serializers import EquipoSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Equipo.objects.filter(liga__admin=self.request.user)
