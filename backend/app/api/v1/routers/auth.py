from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, PasswordChange, UserRead
from app.services.user_service import authenticate_user, create_user, change_user_password

router = APIRouter()

@router.get("/status")
async def auth_status():
    return {"success": True, "data": {"message": "Auth structure preparada"}}

@router.post("/register", response_model=dict)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await create_user(db, user_in)
        return {"success": True, "data": UserRead.from_orm(user)}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.post("/login", response_model=dict)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, credentials.email, credentials.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return {"success": True, "data": UserRead.from_orm(user)}

@router.post("/change-password", response_model=dict)
async def change_password(data: PasswordChange, db: AsyncSession = Depends(get_db)):
    user = await change_user_password(db, data.email, data.current_password, data.new_password)
    if user is None:
        raise HTTPException(status_code=401, detail="Email o contraseña actual incorrectos")
    return {"success": True, "data": {"message": "Contraseña actualizada correctamente"}}
