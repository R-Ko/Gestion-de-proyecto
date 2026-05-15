from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()

@router.get("/projects/{project_id}/tasks", response_model=dict)
async def get_project_tasks(project_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await TaskService.list_tasks(db, project_id)
    return {"success": True, "data": tasks}

@router.get("/tasks/{task_id}", response_model=dict)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await TaskService.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"success": True, "data": task}

@router.post("/tasks", response_model=dict)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await TaskService.create_task(db, payload)
    return {"success": True, "data": task}

@router.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: int, payload: TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await TaskService.update_task(db, task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"success": True, "data": task}

@router.patch("/tasks/{task_id}/status", response_model=dict)
async def patch_task_status(task_id: int, status: str, db: AsyncSession = Depends(get_db)):
    task = await TaskService.update_status(db, task_id, status)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"success": True, "data": task}

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await TaskService.delete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"success": True, "data": {"id": task_id}}
