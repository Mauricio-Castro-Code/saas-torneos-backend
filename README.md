# saas-torneos-backend

API backend (Django + Django REST Framework) para un SaaS de gestión de ligas deportivas amateur (fútbol 7, tochito). Administra ligas, equipos, jugadores, jornadas y resultados para organizadores que hoy usan Excel + WhatsApp.

## Stack
- Django + Django REST Framework
- PostgreSQL
- JWT (`djangorestframework-simplejwt`) + login con Google (`django-allauth`)
- Deploy en Railway

## Requisitos
- Python 3.11+
- PostgreSQL (local o conexión a Railway)

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Variables de entorno

Copia `.env.example` a `.env` y llena:

```
DATABASE_URL=postgres://usuario:password@localhost:5432/saas_torneos
SECRET_KEY=
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
```

## Estructura del proyecto

```
config/       # settings de Django
accounts/     # usuario custom, roles, auth (JWT + Google)
leagues/      # liga, temporada, código de join
teams/        # equipo, jugador
matches/      # jornada, partido, estadísticas
```

## Roles
`admin` (administrador de liga), `capitan`, `jugador`. Detalle completo de reglas de negocio, flujo de auth/join y convenciones en `CLAUDE.md`.

## Cómo trabajamos en equipo
Ver `CONTRIBUTING.md` — flujo de ramas, Pull Requests y revisión.

## Deploy
Automático a Railway en cada push a `main`.