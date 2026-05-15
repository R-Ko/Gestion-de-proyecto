from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.password import hash_password, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_list(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("El email ya está registrado")

    user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        role=user_in.role,
        is_active=user_in.is_active,
        avatar_url=user_in.avatar_url,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user is None or user.password_hash is None:
        return None
    if verify_password(password, user.password_hash):
        return user
    return None


async def change_user_password(db: AsyncSession, email: str, current_password: str, new_password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user is None or user.password_hash is None:
        return None
    if not verify_password(current_password, user.password_hash):
        return None
    user.password_hash = hash_password(new_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
