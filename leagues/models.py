import random
import string

from django.conf import settings
from django.db import models


def generar_codigo_liga():
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    sufijo = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{letras}-{sufijo}"


class Liga(models.Model):
    class Formato(models.TextChoices):
        LIGA = "liga", "Liga (ida y vuelta)"
        LIGUILLA = "liguilla", "Liguilla (una vuelta + eliminatorias)"

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=8, unique=True, editable=False)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ligas"
    )
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    sede = models.CharField(max_length=255, blank=True)
    formato = models.CharField(max_length=10, choices=Formato.choices, default=Formato.LIGA)
    # Cupos manual por ahora (elegido por el admin al crear la liga). El límite
    # por tier de suscripción (CLAUDE.md) es una validación futura, todavía no
    # se enforce en ningún lado -- este campo no la reemplaza.
    cupos_maximos = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            codigo = generar_codigo_liga()
            while Liga.objects.filter(codigo=codigo).exists():
                codigo = generar_codigo_liga()
            self.codigo = codigo
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
