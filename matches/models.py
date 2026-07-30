from django.db import models

from leagues.models import Liga


class Temporada(models.Model):
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name="temporadas")
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.liga.nombre})"


class Categoria(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="categorias")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.temporada}"


class Jornada(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="jornadas")
    numero = models.PositiveIntegerField()
    fecha = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"Jornada {self.numero} - {self.categoria}"


class Partido(models.Model):
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, related_name="partidos")
    equipo_local = models.ForeignKey(
        "teams.Equipo", on_delete=models.CASCADE, related_name="partidos_local"
    )
    equipo_visitante = models.ForeignKey(
        "teams.Equipo", on_delete=models.CASCADE, related_name="partidos_visitante"
    )
    cancha = models.CharField(max_length=100, blank=True)
    horario = models.DateTimeField(null=True, blank=True)
    nombre_arbitro = models.CharField(max_length=100, blank=True)
    goles_local = models.PositiveIntegerField(null=True, blank=True)
    goles_visitante = models.PositiveIntegerField(null=True, blank=True)

    @property
    def jugado(self):
        return self.goles_local is not None and self.goles_visitante is not None

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"
