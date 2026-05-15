from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity
from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity import ActivityCreate

class ActivityService:
    @staticmethod
    async def list_activities(session: AsyncSession, task_id: int):
        return await ActivityRepository.get_by_task(session, task_id)

    @staticmethod
    async def create_activity(session: AsyncSession, payload: ActivityCreate):
        activity = Activity(**payload.model_dump())
        return await ActivityRepository.create(session, activity)
