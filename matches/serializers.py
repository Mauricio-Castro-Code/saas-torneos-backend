from rest_framework import serializers

from .models import Categoria, Temporada


class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = ["id", "liga", "nombre", "fecha_inicio", "fecha_fin", "activa"]

    def validate_liga(self, liga):
        request = self.context["request"]
        if liga.admin_id != request.user.id:
            raise serializers.ValidationError(
                "No puedes crear temporadas en una liga que no administras."
            )
        return liga


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "temporada", "nombre"]

    def validate_temporada(self, temporada):
        request = self.context["request"]
        if temporada.liga.admin_id != request.user.id:
            raise serializers.ValidationError(
                "No puedes crear categorías en una temporada que no administras."
            )
        return temporada
