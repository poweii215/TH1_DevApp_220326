from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.todo_model import Todo


class TodoService:
    def __init__(self, repository):
        self.repository = repository

    def create_todo(self, db: Session, data):
        return self.repository.create(
            db=db,
            title=data.title,
            description=data.description,
            is_done=data.is_done
        )

    def get_todo(self, db: Session, todo_id: int):
        return self.repository.get_by_id(db, todo_id)

    def update_todo(self, db: Session, todo_id: int, data):
        todo = self.repository.get_by_id(db, todo_id)
        if not todo:
            return None

        return self.repository.update(
            db=db,
            todo=todo,
            title=data.title,
            description=data.description,
            is_done=data.is_done
        )

    def delete_todo(self, db: Session, todo_id: int):
        todo = self.repository.get_by_id(db, todo_id)
        if not todo:
            return None

        return self.repository.delete(db, todo)
    
    def update_status(self, db: Session, todo_id: int, is_done: bool):
        todo = self.repository.get_by_id(db, todo_id)
        if not todo:
            return None

        todo.is_done = is_done
        db.commit()
        db.refresh(todo)
        return todo


    def mark_complete(self, db: Session, todo_id: int):
        todo = self.repository.get_by_id(db, todo_id)
        if not todo:
            return None

        todo.is_done = True
        db.commit()
        db.refresh(todo)
        return todo


    def list_todos(
        self,
        db: Session,
        is_done: bool | None = None,
        q: str | None = None,
        sort: str = "created_at",
        limit: int = 10,
        offset: int = 0,
    ):
        query = db.query(Todo)

        # Filter
        if is_done is not None:
            query = query.filter(Todo.is_done == is_done)

        # Search
        if q:
            query = query.filter(Todo.title.ilike(f"%{q}%"))

        # Sort
        if sort.startswith("-"):
            field_name = sort[1:]
            field = getattr(Todo, field_name, Todo.created_at)
            query = query.order_by(desc(field))
        else:
            field = getattr(Todo, sort, Todo.created_at)
            query = query.order_by(asc(field))

        total = query.count()

        # Pagination
        items = query.offset(offset).limit(limit).all()

        return items, total
