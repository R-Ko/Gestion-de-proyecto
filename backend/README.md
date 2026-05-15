# Gestión de Proyecto Backend

Backend de la aplicación de gestión de proyectos y tareas con FastAPI, PostgreSQL, SQLAlchemy 2 y Pydantic v2.

## Estructura

- `app/main.py`: punto de entrada FastAPI.
- `app/api/v1/routers`: routers por recursos.
- `app/models`: modelos SQLAlchemy.
- `app/schemas`: Pydantic schemas.
- `app/services`: lógica de negocio.
- `app/repositories`: acceso a datos.
- `app/db`: configuración de base de datos.
- `alembic`: migraciones.

## Requisitos

- Python 3.12
- PostgreSQL

## Instalación

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Copia `.env.example` a `.env` y ajusta `DATABASE_URL`.

## Ejecutar

```bash
uvicorn app.main:app --reload
```

## Migraciones

```bash
alembic upgrade head
```

## Seed

```bash
python -m app.db.init_db
```
