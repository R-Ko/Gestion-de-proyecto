from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(500), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(String(100), nullable=False, default="usuario")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    assigned_projects = relationship("Project", secondary="user_projects", back_populates="assigned_users")
