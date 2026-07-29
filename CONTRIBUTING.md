# Flujo de trabajo en equipo

Esta guía cubre cómo nos organizamos, cómo dejamos el entorno listo en cada máquina, y el ciclo completo de cada tarea desde que se crea hasta que llega a `main` — con el porqué de cada paso, no solo el comando.

---

## División de módulos

Para evitar pisarnos, cada quien trabaja en carpetas/apps distintas la mayor parte del tiempo:

**Backend:**
- Mauricio: `accounts` (auth, JWT, login con Google), `leagues` (liga, código de join)
- Jorge: `teams` (equipos, jugadores), `matches` (jornadas, partidos, resultados)

**Frontend:**
- Mauricio: `admin/`, `auth/`
- Jorge: `capitan/`, `jugador/`

**Por qué:** dividir por dominio (no por "front vs back" a secas) significa que casi nunca tocan el mismo archivo al mismo tiempo — eso es lo que de verdad evita conflictos de merge, más que cualquier comando de Git.

---

## Reglas base

- **Nadie hace commit directo a `main`.** Todo el trabajo vive en una rama.
- Ramas de vida corta (1-2 días máximo) — entre más tiempo vive una rama sin mergear, peor el conflicto al juntarla.
- Commits chicos y frecuentes, con mensajes descriptivos (`feat: `, `fix: `, `refactor: `), no un commit gigante al final del día.
- Nombres de rama: minúsculas, sin espacios ni acentos, separados por guiones (`feature/validar-codigo-liga`, no `feature/Validar Código de Liga`) — un espacio hace que Git interprete el nombre como varios argumentos y truena el comando.

---

## Setup del entorno local (una sola vez, por persona)

Cada quien tiene su **propia base de datos Postgres local**, separada de la del otro — no se comparte una sola instancia entre los dos, cada uno prueba de forma aislada.

```bash
# 1. Levantar Postgres con Docker (recomendado)
docker run --name saas-torneos-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=saas_torneos -p 5432:5432 -d postgres:16

# 2. Clonar el repo
git clone <url-del-repo>
cd <carpeta-del-repo>

# 3. Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 4. Copiar variables de entorno
cp .env.example .env

# 5. Migrar
python manage.py migrate
```

**Por qué cada quien su propia base:** si compartieran una sola base de datos, una migración de uno podría borrar o alterar tablas que el otro está usando para probar en ese momento. Aislado, cada uno puede tronar y resetear su base sin afectar al otro.

**Nota de orden:** el modelo `Usuario` (de `accounts`) debe existir y estar migrado antes de correr migraciones de `teams`/`matches`, porque esos modelos tienen `ForeignKey` hacia `Usuario`.

---

## El ciclo completo: de tarea a `main`

### 1. Crea tu rama para la tarea

```bash
git checkout -b feature/nombre-de-la-tarea
```

**Por qué:** cada tarea vive en su propia rama, nunca se trabaja directo en `main`. Así `main` siempre queda en un estado que funciona, y tu trabajo en progreso no interfiere con el de los demás.

### 2. Escribe el código de la tarea

En los archivos correspondientes según la responsabilidad (ej. `leagues/views.py`, `leagues/serializers.py`, `leagues/urls.py`).

**Por qué la separación por archivo:** cada uno tiene una sola responsabilidad (`models.py` = qué es el dato, `serializers.py` = cómo se convierte a JSON, `views.py` = qué pasa cuando llega un request, `permissions.py` = quién puede tocar qué). Si mañana cambia algo de una capa, tocas un solo archivo sin arriesgar romper las demás.

### 3. Prueba que funcione en local antes de commitear

```bash
python manage.py runserver
# prueba el endpoint con Postman/Thunder Client o curl
```

**Por qué:** un commit no es "guardar", es una declaración de "esto funciona". Si commiteas código roto, quien haga `pull` después hereda el problema sin saberlo.

### 4. Commit — chico y descriptivo

```bash
git add .
git commit -m "feat: descripción corta de lo que hiciste"
```

**Por qué chico y frecuente:** si algo se rompe después, es fácil encontrar en cuál commit específico pasó, en vez de revisar cientos de líneas de cambios mezclados.

### 5. Antes de subir, trae lo que haya cambiado en `main`

```bash
git pull origin main --rebase
```

**Por qué:** si el otro ya subió algo a `main` mientras trabajabas, tu rama quedó desactualizada. El `--rebase` reacomoda tus commits ENCIMA de lo nuevo, sin crear un commit de merge feo en medio del historial. Si hay conflicto, aparece aquí — chico y fácil de resolver, mejor que dejarlo acumular.

### 6. Sube tu rama

```bash
git push -u origin feature/nombre-de-la-tarea
```
(la primera vez con `-u`; después solo `git push`)

### 7. Abre el Pull Request en GitHub

- Describe qué hiciste
- Asigna al otro como reviewer
- Espera aprobación antes de mergear — este es el punto de control real del equipo

**Por qué:** el PR es la última oportunidad de que alguien más atrape un bug o una decisión rara antes de que viva en `main` y le rompa el trabajo a los demás. No es trámite, es la revisión real.

### 8. Revisar el PR del otro — no es solo dar "Approve" a ciegas

```bash
git fetch origin
git worktree add ../<repo>-review feature/su-rama
cd ../<repo>-review
python manage.py migrate
python manage.py runserver
# prueba el endpoint de verdad: casos válidos, inválidos, de error
```

Checklist antes de aprobar:
- ¿Corre sin errores?
- ¿Sigue la estructura acordada (`models.py`/`serializers.py`/`views.py` separados)?
- ¿Nombres en `snake_case` (Python) o `camelCase`/`PascalCase` (Angular) según corresponda?
- ¿Hay algo hardcodeado que debería ser variable de entorno?

Revisa también el código en "Files changed" en GitHub, comenta línea por línea si algo no queda claro. Si todo bien, **"Approve"**. Si falta algo, **"Request changes"** con el comentario — se corrige en la misma rama, se hace push de nuevo, y el PR se actualiza solo.

`git worktree` te deja tener la rama del otro corriendo en una carpeta aparte sin perder tu propio trabajo en progreso ni tener que hacer `stash`.

### 9. Mergear — usar "Squash and merge" en GitHub

**Por qué:** convierte todos los commits chicos de la rama ("wip", "fix", "otro fix") en uno solo, limpio, en `main`. El historial queda legible — cualquiera puede ver la lista de commits y entender qué se construyó.

### 10. Después de mergear, limpiar

```bash
git checkout main
git pull
git branch -d feature/nombre-de-la-tarea
```

**Por qué:** una rama ya mergeada no sirve para nada más — dejarla viva solo genera ruido cuando alguien hace `git branch` y ve un montón de ramas sin saber cuáles siguen activas.

---

## Resumen visual del ciclo completo

```
main (protegida)
  └─ checkout -b feature/tarea
       → código → probar local → commit
       → pull --rebase → push
       → Pull Request → review (worktree + checklist)
       → squash merge → main
       → limpiar rama local
```

Cada tarea nueva del sprint sigue exactamente este mismo ciclo.