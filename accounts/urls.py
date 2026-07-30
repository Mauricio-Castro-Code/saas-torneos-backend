from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, RegistroAdminView, RegistroJugadorView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path("registro/admin/", RegistroAdminView.as_view(), name="registro_admin"),
    path("registro/jugador/", RegistroJugadorView.as_view(), name="registro_jugador"),
]
