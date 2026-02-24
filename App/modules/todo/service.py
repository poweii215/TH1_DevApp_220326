from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.modules.todo.model import Tag, Todo


class TodoService:
    def __init__(self, repository):
        self.repository = repository

    def create_todo(self, db: Session, data, user_id: int):
        tag_objects = []
        if data.tags:
            for tag_name in data.tags:
                normalized_name = tag_name.strip().lower()
                if not normalized_name:
                    continue
                tag = db.query(Tag).filter(Tag.name == normalized_name).first()
                if not tag:
                    tag = Tag(name=normalized_name)
                    db.add(tag)
                    db.flush()  
                tag_objects.append(tag)

        due_date = None
        if data.due_date:
            if not isinstance(data.due_date, datetime):
                raise ValueError("due_date must be a valid datetime")
            if data.due_date < datetime.now(timezone.utc):
                raise ValueError("due_date cannot be in the past")
            due_date = data.due_date
        return self.repository.create(
            db=db,
            title=data.title,
            description=data.description,
            is_done=data.is_done,
            due_date=due_date,
            owner_id=user_id,
            tags=tag_objects
        )

    def get_todo(self, db: Session, todo_id: int, owner_id: int):
        return self.repository.get_by_id(db, todo_id, owner_id)

    def update_todo(self, db: Session, todo_id: int, data, owner_id: int):
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if not todo:
            return None

        return self.repository.update(
            db=db,
            todo=todo,
            title=data.title,
            description=data.description,
            is_done=data.is_done,
            tags =data.tags,
            due_date=data.due_date
        )

    def delete_todo(self, db: Session, todo_id: int, owner_id: int):
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if not todo:
            return None
        return self.repository.delete(db, todo)

    def mark_complete(self, db: Session, todo_id: int, owner_id: int):
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if not todo:
            return None

        todo.is_done = True
        db.commit()
        db.refresh(todo)
        return todo

    def list_todos(
        self,
        db: Session,
        owner_id: int,
        is_done: bool | None = None,
        q: str | None = None,
        sort: str = "created_at",
        limit: int = 10,
        offset: int = 0,
    ):
        query = db.query(Todo).filter(Todo.owner_id == owner_id)

        if is_done is not None:
            query = query.filter(Todo.is_done == is_done)

        if q:
            query = query.filter(Todo.title.ilike(f"%{q}%"))

        if sort.startswith("-"):
            field_name = sort[1:]
            field = getattr(Todo, field_name, Todo.created_at)
            query = query.order_by(desc(field))
        else:
            field = getattr(Todo, sort, Todo.created_at)
            query = query.order_by(asc(field))

        total = query.count()
        items = query.offset(offset).limit(limit).all()

        return items, total
    
    
    def get_overdue(self, db, current_user):
        return db.query(Todo).filter(
            Todo.owner_id == current_user.id,
            Todo.due_date < datetime.utcnow()
        ).all()


    def get_today(self,db, current_user):
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        return db.query(Todo).filter(
            Todo.owner_id == current_user.id,
            Todo.due_date >= today_start,
            Todo.due_date < today_end
        ).all()
   