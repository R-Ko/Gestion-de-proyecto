from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity

class ActivityRepository:
    @staticmethod
    async def get_by_task(session: AsyncSession, task_id: int):
        result = await session.execute(select(Activity).where(Activity.task_id == task_id).order_by(Activity.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def create(session: AsyncSession, activity: Activity):
        session.add(activity)
        await session.commit()
        await session.refresh(activity)
        return activity
