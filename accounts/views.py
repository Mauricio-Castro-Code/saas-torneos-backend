from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UsuarioTokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    serializer_class = UsuarioTokenObtainPairSerializer
