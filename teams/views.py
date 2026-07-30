from django.db import IntegrityError, transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from leagues.models import Liga
from leagues.permissions import EsAdmin

from .models import Equipo, Jugador
from .permissions import EsCapitanDeSuEquipo, EsJugador
from .serializers import EquipoCapitanSerializer, EquipoPublicoSerializer, EquipoSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_queryset(self):
        return Equipo.objects.filter(liga__admin=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        url_path="por_liga/(?P<codigo>[^/.]+)",
        permission_classes=[AllowAny],
    )
    def por_liga(self, request, codigo=None):
        equipos = Equipo.objects.filter(liga__codigo=codigo.upper(), liga__activa=True)
        return Response(EquipoPublicoSerializer(equipos, many=True).data)

    @action(
        detail=False,
        methods=["post"],
        url_path="unirse",
        permission_classes=[IsAuthenticated, EsJugador],
    )
    def unirse(self, request):
        codigo_liga = request.data.get("codigo_liga", "")
        equipo_id = request.data.get("equipo_id")

        try:
            liga = Liga.objects.get(codigo=codigo_liga.upper(), activa=True)
        except Liga.DoesNotExist:
            return Response(
                {"detail": "Código de liga inválido."}, status=status.HTTP_404_NOT_FOUND
            )

        if Jugador.objects.filter(usuario=request.user).exists():
            return Response(
                {"detail": "Ya perteneces a un equipo."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                try:
                    equipo = Equipo.objects.select_for_update().get(id=equipo_id, liga=liga)
                except Equipo.DoesNotExist:
                    return Response(
                        {"detail": "Ese equipo no existe en la liga indicada."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                es_primero = not equipo.jugadores.exists()
                Jugador.objects.create(equipo=equipo, usuario=request.user)
                if es_primero:
                    equipo.capitan = request.user
                    equipo.save()
        except IntegrityError:
            return Response(
                {"detail": "Ya perteneces a un equipo."}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "equipo": EquipoPublicoSerializer(equipo).data,
                "es_capitan": es_primero,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="mi_equipo",
        permission_classes=[IsAuthenticated, EsCapitanDeSuEquipo],
    )
    def mi_equipo(self, request):
        try:
            equipo = Equipo.objects.get(capitan=request.user)
        except Equipo.DoesNotExist:
            return Response(
                {"detail": "No eres capitán de ningún equipo."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, equipo)

        if request.method == "GET":
            return Response(EquipoCapitanSerializer(equipo).data)

        serializer = EquipoCapitanSerializer(equipo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
