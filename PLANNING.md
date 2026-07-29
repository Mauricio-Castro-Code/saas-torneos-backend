# Sprint 1 — Backend: tareas y setup

## Requisitos previos (ambos)

- Python 3.11+
- Postgres corriendo localmente (Docker o instalación nativa)
- Clonar el repo `saas-torneos-backend`
- Copiar `.env.example` a `.env`

```bash
# Levantar Postgres con Docker (recomendado)
docker run --name saas-torneos-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=saas_torneos -p 5432:5432 -d postgres:16

# Clonar y preparar el entorno
git clone https://github.com/Mauricio-Castro-Code/saas-torneos-backend.git
cd saas-torneos-backend
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-allauth pillow psycopg2-binary dj-database-url python-dotenv
cp .env.example .env
```

## Mauricio — `accounts` + `leagues`

**Debe hacerse primero** (Jorge depende de que exista el modelo `Usuario` antes de migrar sus propios modelos).

| # | Tarea |
|---|---|
| 1 | Setup inicial del proyecto Django — `startproject`, crear las 4 apps, configurar `AUTH_USER_MODEL` antes de la primera migración |
| 2 | Modelo `Usuario` custom (extiende `AbstractUser`, campo `role`: admin/capitan/jugador) |
| 3 | Auth JWT — endpoints login/refresh con `djangorestframework-simplejwt` |
| 4 | Login con Google — integrar `django-allauth` |
| 5 | Modelo `Liga` + generación de código único, endpoint para crearla (solo admin) |
| 6 | Endpoint validar código de liga (público, sin auth) |
| — | Correr `makemigrations` + `migrate` y avisar a Jorge cuando esté listo |

## Jorge — `teams` + `matches`

**Puede empezar en paralelo**, usando un usuario de prueba (`createsuperuser`) mientras Mauricio termina auth. Sus `ForeignKey` hacia `Usuario` necesitan que la migración de Mauricio ya exista antes de correr las suyas.

| # | Tarea |
|---|---|
| 7 | Modelos `Equipo` y `Jugador` (`capitan` nullable en `Equipo`) |
| 8 | Endpoint crear equipo (solo admin, dentro de una liga existente) |
| 9 | Endpoint join a equipo con código — usar `select_for_update()` para que el primer jugador en unirse se vuelva capitán, sin condición de carrera |
| 10 | Permission class `EsCapitanDeSuEquipo` — valida pertenencia, no solo rol |
| 11 | Modelos `Temporada`, `Categoria`, `Jornada`, `Partido` |
| 12 | Endpoint captura de resultados — prioriza pocos clics, es la vista de mayor uso semanal |

## Estructura interna que ambos siguen en cada app

```
<nombre_app>/
├── models.py
├── serializers.py
├── permissions.py
├── views.py
├── urls.py
└── migrations/
```

## Flujo de Git (resumen, ver `CONTRIBUTING.md` para el detalle completo)

```bash
git checkout -b feature/nombre-de-tu-tarea
# ...trabajas, commits chicos...
git pull origin main --rebase   # antes de subir, para traer lo del otro
git push -u origin feature/nombre-de-tu-tarea
# abrir Pull Request, esperar review, squash and merge
```

## Punto de sincronización

Cuando Mauricio termine auth (#2-4) y Jorge esté listo con join a equipo (#9), hacer una sesión corta juntos para probar el flujo completo de punta a punta: crear cuenta → código de liga → unirse a equipo → confirmar rol de capitán asignado.