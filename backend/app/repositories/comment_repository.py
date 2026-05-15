from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment

class CommentRepository:
    @staticmethod
    async def get_by_task(session: AsyncSession, task_id: int):
        result = await session.execute(select(Comment).where(Comment.task_id == task_id).order_by(Comment.created_at))
        return result.scalars().all()

    @staticmethod
    async def create(session: AsyncSession, comment: Comment):
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    @staticmethod
    async def delete(session: AsyncSession, comment: Comment):
        await session.delete(comment)
        await session.commit()
