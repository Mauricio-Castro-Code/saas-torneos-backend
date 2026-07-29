from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Liga
from .permissions import EsAdmin
from .serializers import LigaSerializer


class LigaViewSet(viewsets.ModelViewSet):
    serializer_class = LigaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Liga.objects.filter(admin=self.request.user)

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
