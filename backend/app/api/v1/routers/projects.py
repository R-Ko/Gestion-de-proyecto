from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate, ProjectAssign
from app.services.project_service import ProjectService

router = APIRouter()

@router.get("/", response_model=dict)
async def get_projects(user_id: int | None = Query(None), db: AsyncSession = Depends(get_db)):
    projects = await ProjectService.list_projects(db, user_id)
    return {"success": True, "data": projects}

@router.get("/{project_id}", response_model=dict)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"success": True, "data": project}

@router.post("/", response_model=dict)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.create_project(db, payload)
    return {"success": True, "data": project}

@router.put("/{project_id}", response_model=dict)
async def update_project(project_id: int, payload: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.update_project(db, project_id, payload)
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"success": True, "data": project}

@router.post("/{project_id}/assign", response_model=dict)
async def assign_project(project_id: int, payload: ProjectAssign, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.update_project(db, project_id, ProjectUpdate(assigned_user_ids=payload.user_ids))
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"success": True, "data": project}

@router.delete("/{project_id}", response_model=dict)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.delete_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"success": True, "data": {"id": project_id}}
