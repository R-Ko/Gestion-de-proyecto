from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task

class TaskRepository:
    @staticmethod
    async def get_by_project(session: AsyncSession, project_id: int):
        result = await session.execute(select(Task).where(Task.project_id == project_id).order_by(Task.id))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, task_id: int):
        result = await session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, task: Task):
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def update(session: AsyncSession, task: Task):
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def delete(session: AsyncSession, task: Task):
        await session.delete(task)
        await session.commit()
