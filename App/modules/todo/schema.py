from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional
from datetime import datetime


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool = False
    tags: List[str] = []
    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Title must not be blank")
        return v
    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, tags: List[str]):
        # remove space + lower + remove duplicate
        cleaned = []
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in cleaned:
                cleaned.append(tag)
        return cleaned

class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool = False
    tags: List[str]
    due_date: Optional[datetime] = None

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
    tags: List[str]
    due_date: datetime | None
    created_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def convert_tags(cls, v):
        # Khi lấy từ ORM: v là list[Tag]
        return [tag.name for tag in v]
    class Config:
        from_attributes = True


class PaginatedTodoResponse(BaseModel):
    items: List[TodoResponse]
    total: int
    limit: int
    offset: int