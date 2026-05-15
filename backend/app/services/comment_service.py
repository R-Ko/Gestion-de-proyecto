from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate

class CommentService:
    @staticmethod
    async def list_comments(session: AsyncSession, task_id: int):
        return await CommentRepository.get_by_task(session, task_id)

    @staticmethod
    async def create_comment(session: AsyncSession, payload: CommentCreate):
        comment = Comment(**payload.model_dump())
        return await CommentRepository.create(session, comment)

    @staticmethod
    async def delete_comment(session: AsyncSession, comment_id: int):
        result = await session.get(Comment, comment_id)
        if result is None:
            return None
        await CommentRepository.delete(session, result)
        return result
