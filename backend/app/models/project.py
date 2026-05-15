from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

user_project_association = Table(
    "user_projects",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(String(800), nullable=True)
    business_type = Column(String(100), nullable=True)
    product_line = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="Planificado")
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    last_log_date = Column(DateTime(timezone=True), nullable=True)
    task_count = Column(Integer, default=0)
    ticket_count = Column(Integer, default=0)
    assigned_users = relationship("User", secondary=user_project_association, back_populates="assigned_projects")

    @property
    def assigned_user_ids(self) -> list[int]:
        return [user.id for user in self.assigned_users]
