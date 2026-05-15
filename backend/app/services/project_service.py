from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    @staticmethod
    async def list_projects(session: AsyncSession, user_id: int | None = None):
        if user_id is not None:
            return await ProjectRepository.get_by_user(session, user_id)
        return await ProjectRepository.get_all(session)

    @staticmethod
    async def get_project(session: AsyncSession, project_id: int):
        return await ProjectRepository.get_by_id(session, project_id)

    @staticmethod
    async def _resolve_users(session: AsyncSession, user_ids: list[int]) -> list[User]:
        if not user_ids:
            return []
        result = await session.execute(select(User).where(User.id.in_(user_ids)))
        return result.scalars().all()

    @staticmethod
    async def create_project(session: AsyncSession, payload: ProjectCreate):
        data = payload.model_dump(exclude_none=True)
        assigned_user_ids = data.pop("assigned_user_ids", [])
        project = Project(**data)
        project.assigned_users = await ProjectService._resolve_users(session, assigned_user_ids)
        return await ProjectRepository.create(session, project)

    @staticmethod
    async def update_project(session: AsyncSession, project_id: int, payload: ProjectUpdate):
        project = await ProjectRepository.get_by_id(session, project_id)
        if project is None:
            return None

        data = payload.model_dump(exclude_none=True)
        assigned_user_ids = data.pop("assigned_user_ids", None)
        for field, value in data.items():
            setattr(project, field, value)

        if assigned_user_ids is not None:
            project.assigned_users = await ProjectService._resolve_users(session, assigned_user_ids)

        return await ProjectRepository.update(session, project)

    @staticmethod
    async def delete_project(session: AsyncSession, project_id: int):
        project = await ProjectRepository.get_by_id(session, project_id)
        if project is None:
            return None
        await ProjectRepository.delete(session, project)
        return project
