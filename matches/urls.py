from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, TemporadaViewSet

router = DefaultRouter()
router.register("temporadas", TemporadaViewSet, basename="temporada")
router.register("categorias", CategoriaViewSet, basename="categoria")

urlpatterns = router.urls
