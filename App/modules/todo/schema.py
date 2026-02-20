from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Title must not be blank")
        return v


class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Title must not be blank")
        return v


class TodoStatusUpdate(BaseModel):
    is_done: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedTodoResponse(BaseModel):
    items: List[TodoResponse]
    total: int
    limit: int
    offset: int