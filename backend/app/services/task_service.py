from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    async def list_tasks(session: AsyncSession, project_id: int):
        return await TaskRepository.get_by_project(session, project_id)

    @staticmethod
    async def get_task(session: AsyncSession, task_id: int):
        return await TaskRepository.get_by_id(session, task_id)

    @staticmethod
    async def create_task(session: AsyncSession, payload: TaskCreate):
        task = Task(**payload.model_dump())
        return await TaskRepository.create(session, task)

    @staticmethod
    async def update_task(session: AsyncSession, task_id: int, payload: TaskUpdate):
        task = await TaskRepository.get_by_id(session, task_id)
        if task is None:
            return None
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(task, field, value)
        return await TaskRepository.update(session, task)

    @staticmethod
    async def update_status(session: AsyncSession, task_id: int, status: str):
        task = await TaskRepository.get_by_id(session, task_id)
        if task is None:
            return None
        task.status = status
        return await TaskRepository.update(session, task)

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int):
        task = await TaskRepository.get_by_id(session, task_id)
        if task is None:
            return None
        await TaskRepository.delete(session, task)
        return task
