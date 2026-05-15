from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.comment import CommentCreate
from app.services.comment_service import CommentService

router = APIRouter()

@router.get("/tasks/{task_id}/comments", response_model=dict)
async def get_comments(task_id: int, db: AsyncSession = Depends(get_db)):
    comments = await CommentService.list_comments(db, task_id)
    return {"success": True, "data": comments}

@router.post("/tasks/{task_id}/comments", response_model=dict)
async def create_comment(task_id: int, payload: CommentCreate, db: AsyncSession = Depends(get_db)):
    if payload.task_id != task_id:
        raise HTTPException(status_code=400, detail="El task_id debe coincidir")
    comment = await CommentService.create_comment(db, payload)
    return {"success": True, "data": comment}

@router.delete("/comments/{comment_id}", response_model=dict)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await CommentService.delete_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {"success": True, "data": {"id": comment_id}}
