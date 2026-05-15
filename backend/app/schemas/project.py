from datetime import datetime
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    code: str
    description: str | None = None
    business_type: str | None = None
    product_line: str | None = None
    status: str | None = "Planificado"
    is_favorite: bool = False
    task_count: int = 0
    ticket_count: int = 0

class ProjectCreate(ProjectBase):
    assigned_user_ids: list[int] = []

class ProjectUpdate(ProjectBase):
    assigned_user_ids: list[int] | None = None

class ProjectAssign(BaseModel):
    user_ids: list[int]

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime | None
    updated_at: datetime | None
    last_log_date: datetime | None
    assigned_user_ids: list[int] = []

    class Config:
        orm_mode = True
