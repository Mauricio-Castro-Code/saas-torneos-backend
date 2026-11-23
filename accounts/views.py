from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Usuario
from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegistroAdminSerializer,
    RegistroJugadorSerializer,
    UsuarioTokenObtainPairSerializer,
)

RESET_RESPONSE = {
    "detail": "Si el correo está registrado, te enviamos instrucciones para restablecer tu contraseña."
}


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


class PasswordResetRequestView(APIView):
    """Envía el correo con el enlace de recuperación.

    Siempre responde igual, exista o no el correo, para no revelar qué
    cuentas están registradas.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        usuarios = Usuario.objects.filter(email__iexact=email, is_active=True)
        for usuario in usuarios:
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = default_token_generator.make_token(usuario)
            enlace = f"{settings.FRONTEND_URL}/auth/restablecer-contrasena?uid={uid}&token={token}"
            send_mail(
                subject="Restablecer tu contraseña",
                message=(
                    f"Hola {usuario.username},\n\n"
                    "Recibimos una solicitud para restablecer tu contraseña.\n"
                    f"Ingresa al siguiente enlace para crear una nueva:\n{enlace}\n\n"
                    "Si no fuiste tú, ignora este correo."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
            )

        return Response(RESET_RESPONSE, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """Valida uid+token y guarda la nueva contraseña."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data["user"]
        usuario.set_password(serializer.validated_data["new_password"])
        usuario.save(update_fields=["password"])
        return Response(
            {"detail": "Tu contraseña se actualizó correctamente."}, status=status.HTTP_200_OK
        )
