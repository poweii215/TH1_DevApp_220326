from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, DateTime, Table,)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column("todo_id", ForeignKey("todos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False,)
    due_date = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
    owner = relationship("User", back_populates="todos")
    tags = relationship(
        "Tag",
        secondary=todo_tags,
        back_populates="todos",
        lazy="selectin",  
    )


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    todos = relationship(
        "Todo",
        secondary=todo_tags,
        back_populates="tags",
        lazy="selectin",
    )