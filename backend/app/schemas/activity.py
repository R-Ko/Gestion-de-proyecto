from datetime import datetime
from pydantic import BaseModel

class ActivityBase(BaseModel):
    task_id: int
    user_id: int
    action: str
    details: str | None = None

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int
    created_at: datetime | None

    class Config:
        orm_mode = True
