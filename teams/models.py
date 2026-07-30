from django.conf import settings
from django.db import models


class Equipo(models.Model):
    categoria = models.ForeignKey(
        "matches.Categoria", on_delete=models.CASCADE, related_name="equipos"
    )
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="equipos/logos/", blank=True, null=True)
    capitan = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipos_capitaneados",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="jugadores")
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jugador_perfil"
    )
    unido_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.equipo}"
