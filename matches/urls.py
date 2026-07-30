from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, JornadaViewSet, PartidoViewSet, TemporadaViewSet

router = DefaultRouter()
router.register("temporadas", TemporadaViewSet, basename="temporada")
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("jornadas", JornadaViewSet, basename="jornada")
router.register("partidos", PartidoViewSet, basename="partido")

urlpatterns = router.urls
