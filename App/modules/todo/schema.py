from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional
from datetime import datetime


# =========================
# CREATE
# =========================
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False
    tags: List[str] = Field(default_factory=list)   
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
        cleaned = []
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in cleaned:
                cleaned.append(tag)
        return cleaned


# =========================
# UPDATE 
# =========================
class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False
    tags: List[str] = Field(default_factory=list)   
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
        cleaned = []
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in cleaned:
                cleaned.append(tag)
        return cleaned


# =========================
# PATCH status
# =========================
class TodoStatusUpdate(BaseModel):
    is_done: bool


# =========================
# RESPONSE
# =========================
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    tags: List[str]
    due_date: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  

    @field_validator("tags", mode="before")
    @classmethod
    def convert_tags(cls, v):
        return [tag.name for tag in v]


# =========================
# PAGINATION
# =========================
class PaginatedTodoResponse(BaseModel):
    items: List[TodoResponse]
    total: int
    limit: int
    offset: int