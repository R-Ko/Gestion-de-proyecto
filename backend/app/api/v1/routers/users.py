from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_user_list

router = APIRouter()

@router.get("/", response_model=dict)
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await get_user_list(db)
    return {"success": True, "data": [UserRead.from_orm(user) for user in users]}

@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"success": True, "data": UserRead.from_orm(user)}

@router.post("/", response_model=dict)
async def create_new_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await create_user(db, user_in)
        return {"success": True, "data": UserRead.from_orm(user)}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
