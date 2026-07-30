from rest_framework import serializers

from .models import Equipo


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ["id", "liga", "nombre", "logo", "capitan", "creado_en"]
        read_only_fields = ["capitan", "creado_en"]

    def validate_liga(self, liga):
        request = self.context["request"]
        if liga.admin_id != request.user.id:
            raise serializers.ValidationError(
                "No puedes crear equipos en una liga que no administras."
            )
        return liga


class EquipoPublicoSerializer(serializers.ModelSerializer):
    """Para el flujo de join: no expone info administrativa de la liga."""

    class Meta:
        model = Equipo
        fields = ["id", "nombre", "logo", "capitan"]


class EquipoCapitanSerializer(serializers.ModelSerializer):
    """El capitan solo puede editar nombre/logo de su equipo, no liga ni capitan."""

    class Meta:
        model = Equipo
        fields = ["id", "liga", "nombre", "logo", "capitan"]
        read_only_fields = ["liga", "capitan"]
