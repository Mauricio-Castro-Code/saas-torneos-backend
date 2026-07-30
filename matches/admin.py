from django.contrib import admin

from .models import Categoria, Jornada, Partido, Temporada


@admin.register(Temporada)
class TemporadaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "liga", "activa", "fecha_inicio", "fecha_fin"]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "temporada"]


@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display = ["numero", "categoria", "fecha"]


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ["equipo_local", "equipo_visitante", "jornada", "horario", "cancha"]
