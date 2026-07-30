# Contexto del proyecto — Backend (Django)

## Qué es esto
SaaS para organizadores de torneos amateur de fútbol/tochito en México (Puebla). Los organizadores (dueños de complejos deportivos, ligas independientes) pagan una suscripción mensual para gestionar sus ligas: jornadas, resultados, tabla de posiciones, equipos y jugadores, en vez de usar Excel + WhatsApp.

Este repo es SOLO el backend. El frontend vive en un repo separado (Angular) y consume esta API vía REST. No hay código compartido entre ambos repos.

## Stack
- **Django** + **Django REST Framework** (DRF) para la API
- **PostgreSQL** como base de datos
- **djangorestframework-simplejwt** para autenticación JWT
- Deploy en **Railway**

## Roles del sistema (RBAC)
Tres roles, un campo `role` en el modelo `Usuario` custom (no por-liga, es un rol global del usuario para el MVP):

- **admin** — administrador de la liga. Crea ligas, temporadas, equipos, jornadas, captura resultados, genera el código de join.
- **capitan** — edita la info de SU equipo (nombre, logo). No puede tocar equipos ajenos.
- **jugador** — solo lectura de estadísticas propias y de la liga, jornadas y horarios.

**IMPORTANTE — no existe rol de árbitro.** Los árbitros solo pitan partidos, no tienen acceso a la app. Si necesitas guardar el nombre del árbitro asignado a un partido, es un campo de texto simple en el modelo `Partido`, no un usuario del sistema.

**IMPORTANTE — no hay votación/predicción de partidos.** Se evaluó y se descartó explícitamente. No construyas un modelo `Prediccion` ni endpoints de votar.

## Regla de negocio crítica: validar pertenencia, no solo rol
El error más común en apps con roles: validar que alguien "es capitán" pero no que "es capitán DE ESE equipo". Cada permission class que toque un objeto de equipo/jugador debe validar `equipo.capitan_id == request.user.id`, no solo `request.user.role == "capitan"`. Ejemplo:

```python
class EsCapitanDeSuEquipo(BasePermission):
    def has_object_permission(self, request, view, obj):
        equipo = obj if isinstance(obj, Equipo) else obj.equipo
        return equipo.capitan_id == request.user.id
```

Esto aplica también en `get_queryset()` para proteger el LIST, no solo el detalle.

## Flujo de alta — MUY IMPORTANTE, no es lo que asumirías por defecto
1. El **admin** crea la liga y genera un **código único por liga** (ej. `PUE-7A3F`).
2. El **admin** crea los equipos directamente dentro de la liga (nombre, logo). Los equipos existen SIN capitán al momento de crearse.
3. Un **jugador** crea su cuenta (usuario/correo/contraseña, sin código todavía), y en un paso posterior separado ingresa el código de liga, ve la lista de equipos ya existentes de esa liga, y elige uno para unirse. **Entra directo, sin aprobación de nadie.**
4. **El primer jugador en unirse a un equipo se convierte en su capitán automáticamente.**

No hay flujo de "solicitud pendiente" ni de invitación por correo — todo es autoservicio con código.

### Cuidado con condición de carrera en el paso 4
Si dos jugadores se unen al mismo equipo vacío casi simultáneamente, ambos podrían calificar como "el primero". Usa `select_for_update()` dentro de una transacción:

```python
from django.db import transaction

def unirse_a_equipo(usuario, equipo_id):
    with transaction.atomic():
        equipo = Equipo.objects.select_for_update().get(id=equipo_id)
        es_primero = not equipo.jugadores.exists()
        jugador = Jugador.objects.create(equipo=equipo, usuario=usuario)
        if es_primero:
            equipo.capitan = usuario
            equipo.save()
    return jugador
```

## Modelo de datos (jerarquía)
```
Liga (tenant, tiene código único)
 └─ Temporada
     └─ Categoría (ej. Libre, Femenil, +35)
         └─ Equipo (capitan puede ser null hasta el primer join)
             └─ Jugador
         └─ Jornada
             └─ Partido (equipo_local, equipo_visitante, cancha, horario, nombre_arbitro como texto)
                 └─ Estadística_partido (goles, tarjetas, MVP)
```

`Usuario` es un modelo custom que extiende `AbstractUser`, con campo `role`. **`AUTH_USER_MODEL` debe configurarse ANTES de la primera migración** — no se puede cambiar después sin migración dolorosa.

## Límites por tier de suscripción (enforcement en código, no solo en UI)
- **Starter** ($400 MXN/mes): 1 liga activa, máx. 20 equipos por liga, máx. 15 jugadores por equipo
- **Pro** ($1,400 MXN/mes): hasta 3 ligas, mismos topes de equipos/jugadores por liga
- **Complejo** (desde $2,800 MXN/mes, cotizado): ligas y equipos ilimitados

Estos límites deben validarse en el backend (no solo ocultar botones en el front) — ej. al crear un equipo, verificar `liga.equipos.count() < limite_del_tier` antes de permitir el alta.

## Convenciones de código
- `snake_case` para variables, funciones, nombres de archivo Python
- Comentarios que expliquen el **por qué**, no el qué (el código ya dice qué hace)
- Apps de Django separadas por dominio: `accounts`, `leagues`, `teams`, `matches` — no una app monolítica `core`
- Usar `ViewSet` + `Router` de DRF para los endpoints CRUD estándar

## ❓ Preguntas abiertas — contéstalas aquí mismo antes de que Claude Code asuma algo

- **Base de datos: ¿Supabase o Postgres nativo de Railway?** Aún no decidido. Si es Supabase, usar el connection string del pooler de SESIÓN, no el de transacción (rompe prepared statements de Django).
- **¿Cómo se cobra la suscripción?** No se ha decidido pasarela de pago (Stripe, Conekta, Mercado Pago) ni si el cobro es automático (recurrente vía tarjeta guardada) o manual (el admin transfiere y tú activas el tier a mano mientras validas el modelo). Esto afecta si necesitas modelar `Suscripcion`/`Pago` desde ya o lo pospones.
- **Notificaciones automáticas (feature de tier Pro):** ¿WhatsApp Business API, push notifications de la PWA, o ambos? No decidido.
- **Login con Google:** considerado, no prioritario para v1. Si lo agregas, usar `django-allauth`.