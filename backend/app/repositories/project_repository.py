from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.models.user import User

class ProjectRepository:
    @staticmethod
    async def get_all(session: AsyncSession):
        result = await session.execute(
            select(Project).options(selectinload(Project.assigned_users)).order_by(Project.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_user(session: AsyncSession, user_id: int):
        result = await session.execute(
            select(Project)
            .join(Project.assigned_users)
            .where(User.id == user_id)
            .options(selectinload(Project.assigned_users))
            .order_by(Project.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, project_id: int):
        result = await session.execute(
            select(Project).where(Project.id == project_id).options(selectinload(Project.assigned_users))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, project: Project):
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    @staticmethod
    async def update(session: AsyncSession, project: Project):
        await session.commit()
        await session.refresh(project)
        return project

    @staticmethod
    async def delete(session: AsyncSession, project: Project):
        await session.delete(project)
        await session.commit()
