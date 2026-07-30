from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from leagues.models import Liga

from .models import Usuario


class UsuarioTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        return token


class _RegistroBaseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "password"]

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value


class RegistroAdminSerializer(_RegistroBaseSerializer):
    def create(self, validated_data):
        return Usuario.objects.create_user(role=Usuario.Role.ADMIN, **validated_data)


class RegistroJugadorSerializer(_RegistroBaseSerializer):
    codigo_liga = serializers.CharField(write_only=True)

    class Meta(_RegistroBaseSerializer.Meta):
        fields = _RegistroBaseSerializer.Meta.fields + ["codigo_liga"]

    def validate_codigo_liga(self, value):
        if not Liga.objects.filter(codigo=value.upper(), activa=True).exists():
            raise serializers.ValidationError("Código de liga inválido.")
        return value.upper()

    def create(self, validated_data):
        validated_data.pop("codigo_liga")
        return Usuario.objects.create_user(role=Usuario.Role.JUGADOR, **validated_data)
