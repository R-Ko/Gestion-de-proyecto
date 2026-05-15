import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.db.base import Base
from app.models.project import Project
from app.models.task import Task
from app.models.comment import Comment
from app.models.activity import Activity
from app.models.user import User

async def init_database() -> None:
    engine = create_async_engine(settings.database_url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = AsyncSession(engine, expire_on_commit=False)
    async with async_session as session:
        users = [
            User(full_name="Ana Romero", email="ana@empresa.com", role="manager", avatar_url=""),
            User(full_name="Carlos Vega", email="carlos@empresa.com", role="developer", avatar_url=""),
        ]
        session.add_all(users)
        await session.flush()

        projects = [
            Project(
                name="Migración ERP",
                code="ERP-001",
                description="Implementación de nuevo módulo financiero.",
                business_type="Consultoría",
                product_line="ERP Core",
                status="Activo",
                is_favorite=True,
                task_count=12,
                ticket_count=4,
            ),
            Project(
                name="Dashboard Comercial",
                code="DASH-002",
                description="Panel de ventas para gerencia.",
                business_type="Software",
                product_line="Analytics",
                status="Planificado",
                is_favorite=False,
                task_count=8,
                ticket_count=2,
            ),
        ]
        session.add_all(projects)
        await session.flush()

        tasks = [
            Task(
                project_id=projects[0].id,
                title="Definir flujos de aprobación",
                description="Mapear requisitos y estados de integración.",
                status="Backlog",
                priority="Alta",
                assignee_id=users[1].id,
                sprint="S1",
                reminder="2026-06-01",
                start_date="2026-05-10",
                due_date="2026-06-05",
                project_start_date="2026-05-01",
                project_deadline="2026-06-30",
                category="Configuración",
                is_favorite=True,
            ),
        ]
        session.add_all(tasks)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(init_database())
