from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Liga
from .permissions import EsAdmin
from .serializers import LigaPublicaSerializer, LigaSerializer


class LigaViewSet(viewsets.ModelViewSet):
    serializer_class = LigaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Liga.objects.filter(admin=self.request.user)

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        url_path="validar/(?P<codigo>[^/.]+)",
        permission_classes=[AllowAny],
    )
    def validar_codigo(self, request, codigo=None):
        try:
            liga = Liga.objects.get(codigo=codigo.upper(), activa=True)
        except Liga.DoesNotExist:
            return Response(
                {"detail": "Código de liga inválido."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(LigaPublicaSerializer(liga).data)
