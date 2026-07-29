from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        CAPITAN = "capitan", "Capitán"
        JUGADOR = "jugador", "Jugador"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.JUGADOR)
