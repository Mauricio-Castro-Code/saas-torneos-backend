from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from leagues.models import Liga
from leagues.serializers import LigaPublicaSerializer

from .serializers import (
    RegistroAdminSerializer,
    RegistroJugadorSerializer,
    UsuarioTokenObtainPairSerializer,
)


class LoginView(TokenObtainPairView):
    serializer_class = UsuarioTokenObtainPairSerializer


class RegistroAdminView(generics.CreateAPIView):
    serializer_class = RegistroAdminSerializer
    permission_classes = [AllowAny]


class RegistroJugadorView(generics.CreateAPIView):
    """Registra al jugador y valida su código de liga en el mismo paso.

    No une al jugador a un equipo todavía: ese paso depende de los
    modelos Equipo/Jugador (tarea de Jorge, teams#7-9), que aún no existen.
    """

    serializer_class = RegistroJugadorSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        codigo_liga = serializer.validated_data["codigo_liga"]
        usuario = serializer.save()
        liga = Liga.objects.get(codigo=codigo_liga)
        return Response(
            {
                "id": usuario.id,
                "username": usuario.username,
                "role": usuario.role,
                "liga": LigaPublicaSerializer(liga).data,
            },
            status=status.HTTP_201_CREATED,
        )
