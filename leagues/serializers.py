from rest_framework import serializers

from .models import Liga


class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = ["id", "nombre", "codigo", "admin", "activa", "creada_en"]
        read_only_fields = ["codigo", "admin", "activa", "creada_en"]
