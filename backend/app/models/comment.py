from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(1200), nullable=False)
    type = Column(String(50), nullable=False, default="comment")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", backref="comments")
    user = relationship("User", backref="comments")
