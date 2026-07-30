from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

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
    """Registra al jugador (solo cuenta: usuario/correo/contraseña).

    Unirse a una liga y elegir equipo es un paso posterior, separado de
    este registro (ver mockup "Unirse a una Liga" / "Selecciona tu
    equipo"). Ese paso depende de los modelos Equipo/Jugador (tarea de
    Jorge, teams#7-9), que aún no existen; mientras tanto ya existe
    `GET /leagues/ligas/validar/<codigo>/` para validar el código.
    """

    serializer_class = RegistroJugadorSerializer
    permission_classes = [AllowAny]
