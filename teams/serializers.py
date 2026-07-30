from rest_framework import serializers

from .models import Equipo


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ["id", "categoria", "nombre", "logo", "capitan", "creado_en"]
        read_only_fields = ["capitan", "creado_en"]

    def validate_categoria(self, categoria):
        request = self.context["request"]
        if categoria.temporada.liga.admin_id != request.user.id:
            raise serializers.ValidationError(
                "No puedes crear equipos en una categoría que no administras."
            )
        return categoria


class EquipoPublicoSerializer(serializers.ModelSerializer):
    """Para el flujo de join: no expone info administrativa de la liga."""

    class Meta:
        model = Equipo
        fields = ["id", "nombre", "logo", "capitan"]


class EquipoCapitanSerializer(serializers.ModelSerializer):
    """El capitan solo puede editar nombre/logo de su equipo, no categoria ni capitan."""

    class Meta:
        model = Equipo
        fields = ["id", "categoria", "nombre", "logo", "capitan"]
        read_only_fields = ["categoria", "capitan"]
