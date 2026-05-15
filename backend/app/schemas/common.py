from typing import Generic, TypeVar
from pydantic import BaseModel

DataType = TypeVar("DataType")

class ResponseSchema(BaseModel):
    success: bool = True
    data: DataType

class PaginatedResponse(BaseModel):
    success: bool = True
    data: list[DataType]
    pagination: dict

class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 20
    search: str | None = None
    status: str | None = None
    priority: str | None = None
