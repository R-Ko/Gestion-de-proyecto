from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(250), nullable=False)
    description = Column(String(1200), nullable=True)
    status = Column(String(100), nullable=False, default="Backlog")
    priority = Column(String(50), nullable=False, default="Medio")
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sprint = Column(String(100), nullable=True)
    reminder = Column(String(100), nullable=True)
    start_date = Column(String(50), nullable=True)
    due_date = Column(String(50), nullable=True)
    project_start_date = Column(String(50), nullable=True)
    project_deadline = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    project = relationship("Project", backref="tasks")
    assignee = relationship("User", backref="assigned_tasks")
