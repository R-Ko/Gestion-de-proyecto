# Gestión de Proyecto

Aplicación completa de gestión de proyectos y tareas con frontend en Next.js 14 + TypeScript + Tailwind CSS y backend en FastAPI + PostgreSQL + SQLAlchemy 2 + Pydantic v2.

## Carpetas

- `frontend/`: aplicación Next.js App Router.
- `backend/`: API FastAPI modular.

## Instrucciones

1. Configura el backend:
   - Copia `backend/.env.example` a `backend/.env`
   - Ajusta `DATABASE_URL`
2. Instala dependencias:
   - `cd backend && python -m venv .venv && .\.venv\Scripts\activate && pip install -r requirements.txt`
   - `cd frontend && npm install`
3. Inicializa la base de datos:
   - `cd backend && .\.venv\Scripts\activate && alembic upgrade head && python -m app.db.init_db`
4. Ejecuta el backend:
   - `cd backend && .\.venv\Scripts\activate && uvicorn app.main:app --reload`
5. Ejecuta el frontend:
   - `cd frontend && npm run dev`
