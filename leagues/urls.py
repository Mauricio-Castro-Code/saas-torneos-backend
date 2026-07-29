from rest_framework.routers import DefaultRouter

from .views import LigaViewSet

router = DefaultRouter()
router.register("ligas", LigaViewSet, basename="liga")

urlpatterns = router.urls
