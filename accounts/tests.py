import re

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from .models import Usuario

RESET_URL = "/api/auth/password/reset/"
CONFIRM_URL = "/api/auth/password/reset/confirm/"
PASSWORD_NUEVA = "NuevaClave#2026xyz"


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    FRONTEND_URL="http://front.test",
)
class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create_user(
            username="jugador1", email="jugador1@example.com", password="ClaveVieja#2026abc"
        )

    def _enlace_desde_correo(self):
        cuerpo = mail.outbox[0].body
        return re.search(r"http\S+", cuerpo).group(0)

    def _uid_token(self, enlace):
        query = enlace.split("?", 1)[1]
        params = dict(p.split("=", 1) for p in query.split("&"))
        return params["uid"], params["token"]

    def test_solicitud_envia_correo_con_enlace(self):
        resp = self.client.post(RESET_URL, {"email": "jugador1@example.com"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["jugador1@example.com"])
        self.assertTrue(
            self._enlace_desde_correo().startswith("http://front.test/auth/restablecer-contrasena?")
        )

    def test_correo_inexistente_responde_igual_sin_enviar(self):
        resp = self.client.post(RESET_URL, {"email": "nadie@example.com"}, format="json")
        resp_existente = self.client.post(
            RESET_URL, {"email": "jugador1@example.com"}, format="json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), resp_existente.json())
        self.assertEqual(len(mail.outbox), 1)  # solo el correo del usuario existente

    def test_email_invalido_regresa_400(self):
        resp = self.client.post(RESET_URL, {"email": "no-es-correo"}, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_confirmar_cambia_la_contrasena(self):
        self.client.post(RESET_URL, {"email": "jugador1@example.com"}, format="json")
        uid, token = self._uid_token(self._enlace_desde_correo())

        resp = self.client.post(
            CONFIRM_URL,
            {"uid": uid, "token": token, "new_password": PASSWORD_NUEVA},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password(PASSWORD_NUEVA))
        self.assertFalse(self.usuario.check_password("ClaveVieja#2026abc"))

    def test_token_no_se_puede_reusar(self):
        self.client.post(RESET_URL, {"email": "jugador1@example.com"}, format="json")
        uid, token = self._uid_token(self._enlace_desde_correo())
        datos = {"uid": uid, "token": token, "new_password": PASSWORD_NUEVA}

        self.assertEqual(self.client.post(CONFIRM_URL, datos, format="json").status_code, 200)
        resp = self.client.post(CONFIRM_URL, datos, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_token_invalido_regresa_400(self):
        uid = urlsafe_base64_encode(force_bytes(self.usuario.pk))
        resp = self.client.post(
            CONFIRM_URL,
            {"uid": uid, "token": "token-falso", "new_password": PASSWORD_NUEVA},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("token", resp.json())

    def test_uid_invalido_regresa_400(self):
        token = default_token_generator.make_token(self.usuario)
        resp = self.client.post(
            CONFIRM_URL,
            {"uid": "basura!!", "token": token, "new_password": PASSWORD_NUEVA},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_contrasena_debil_regresa_400_y_no_cambia(self):
        self.client.post(RESET_URL, {"email": "jugador1@example.com"}, format="json")
        uid, token = self._uid_token(self._enlace_desde_correo())
        resp = self.client.post(
            CONFIRM_URL,
            {"uid": uid, "token": token, "new_password": "123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("new_password", resp.json())
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("ClaveVieja#2026abc"))

    def test_token_se_invalida_al_cambiar_contrasena_por_otro_medio(self):
        self.client.post(RESET_URL, {"email": "jugador1@example.com"}, format="json")
        uid, token = self._uid_token(self._enlace_desde_correo())
        self.usuario.set_password("OtraClave#2026zzz")
        self.usuario.save()
        resp = self.client.post(
            CONFIRM_URL,
            {"uid": uid, "token": token, "new_password": PASSWORD_NUEVA},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
