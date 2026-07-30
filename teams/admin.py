from django.contrib import admin

from .models import Equipo, Jugador


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria", "capitan", "creado_en"]


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ["usuario", "equipo", "unido_en"]
