from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    message: str
    type: str = "comment"

class CommentCreate(CommentBase):
    task_id: int
    user_id: int

class CommentRead(CommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime | None

    class Config:
        orm_mode = True
