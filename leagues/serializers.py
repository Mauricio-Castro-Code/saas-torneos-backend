from rest_framework import serializers

from .models import Liga


class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = [
            "id",
            "nombre",
            "codigo",
            "admin",
            "activa",
            "creada_en",
            "sede",
            "formato",
            "cupos_maximos",
        ]
        read_only_fields = ["codigo", "admin", "activa", "creada_en"]


class LigaPublicaSerializer(serializers.ModelSerializer):
    """Para el endpoint público de validar código: no expone `admin`."""

    class Meta:
        model = Liga
        fields = ["id", "nombre", "codigo"]
