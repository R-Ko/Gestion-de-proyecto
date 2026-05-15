from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.activity import ActivityCreate
from app.services.activity_service import ActivityService

router = APIRouter()

@router.get("/tasks/{task_id}/activities", response_model=dict)
async def get_activities(task_id: int, db: AsyncSession = Depends(get_db)):
    activities = await ActivityService.list_activities(db, task_id)
    return {"success": True, "data": activities}

@router.post("/tasks/{task_id}/activities", response_model=dict)
async def create_activity(task_id: int, payload: ActivityCreate, db: AsyncSession = Depends(get_db)):
    if payload.task_id != task_id:
        raise HTTPException(status_code=400, detail="El task_id debe coincidir")
    activity = await ActivityService.create_activity(db, payload)
    return {"success": True, "data": activity}
