from rest_framework import serializers

from .models import Categoria, Jornada, Partido, Temporada


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


class JornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada
        fields = ["id", "categoria", "numero", "fecha"]

    def validate_categoria(self, categoria):
        request = self.context["request"]
        if categoria.temporada.liga.admin_id != request.user.id:
            raise serializers.ValidationError(
                "No puedes crear jornadas en una categoría que no administras."
            )
        return categoria


class PartidoSerializer(serializers.ModelSerializer):
    jugado = serializers.BooleanField(read_only=True)
    equipo_local_nombre = serializers.CharField(source="equipo_local.nombre", read_only=True)
    equipo_visitante_nombre = serializers.CharField(source="equipo_visitante.nombre", read_only=True)

    class Meta:
        model = Partido
        fields = [
            "id",
            "jornada",
            "equipo_local",
            "equipo_local_nombre",
            "equipo_visitante",
            "equipo_visitante_nombre",
            "cancha",
            "horario",
            "nombre_arbitro",
            "goles_local",
            "goles_visitante",
            "jugado",
        ]

    def validate_jornada(self, jornada):
        request = self.context["request"]
        if jornada.categoria.temporada.liga.admin_id != request.user.id:
            raise serializers.ValidationError(
                "No puedes crear partidos en una jornada que no administras."
            )
        return jornada

    def validate(self, attrs):
        jornada = attrs.get("jornada", getattr(self.instance, "jornada", None))
        equipo_local = attrs.get("equipo_local", getattr(self.instance, "equipo_local", None))
        equipo_visitante = attrs.get(
            "equipo_visitante", getattr(self.instance, "equipo_visitante", None)
        )

        if equipo_local and equipo_visitante and equipo_local == equipo_visitante:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo.")

        if jornada:
            for equipo in (equipo_local, equipo_visitante):
                if equipo and equipo.categoria_id != jornada.categoria_id:
                    raise serializers.ValidationError(
                        f"{equipo.nombre} no pertenece a la categoría de esta jornada."
                    )

        return attrs
