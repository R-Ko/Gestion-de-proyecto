from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "Backlog"
    priority: str = "Medio"
    assignee_id: int | None = None
    sprint: str | None = None
    reminder: str | None = None
    start_date: str | None = None
    due_date: str | None = None
    project_start_date: str | None = None
    project_deadline: str | None = None
    category: str | None = None
    is_favorite: bool = False

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    project_id: int
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        orm_mode = True
