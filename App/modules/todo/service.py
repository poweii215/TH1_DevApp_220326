from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.modules.todo.model import Tag, Todo


class TodoService:
    def __init__(self, repository):
        self.repository = repository

    # =========================
    # INTERNAL: build tag objects
    # =========================
    def _build_tags(self, db: Session, tag_names: list[str]):
        tag_objects = []

        for tag_name in tag_names:
            normalized = tag_name.strip().lower()
            if not normalized:
                continue

            tag = db.query(Tag).filter(Tag.name == normalized).first()
            if not tag:
                tag = Tag(name=normalized)
                db.add(tag)
                db.flush()

            tag_objects.append(tag)

        return tag_objects


    # =========================
    # CREATE
    # =========================
    def create_todo(self, db: Session, data, user_id: int):

        if data.due_date:
            if data.due_date < datetime.now(timezone.utc):
                raise ValueError("due_date cannot be in the past")

        tag_objects = self._build_tags(db, data.tags)

        return self.repository.create(
            db=db,
            title=data.title,
            description=data.description,
            is_done=data.is_done,
            due_date=data.due_date,
            owner_id=user_id,
            tags=tag_objects,
        )


    # =========================
    # READ
    # =========================
    def get_todo(self, db: Session, todo_id: int, owner_id: int):
        return self.repository.get_by_id(db, todo_id, owner_id)


    # =========================
    # UPDATE
    # =========================
    def update_todo(self, db: Session, todo_id: int, data, owner_id: int):
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if not todo:
            return None

        tag_objects = self._build_tags(db, data.tags)

        return self.repository.update(
            db=db,
            todo=todo,
            title=data.title,
            description=data.description,
            is_done=data.is_done,
            tags=tag_objects,
            due_date=data.due_date,
        )


    # =========================
    # SOFT DELETE
    # =========================
    def delete_todo(self, db: Session, todo_id: int, owner_id: int):
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if not todo:
            return None

        return self.repository.soft_delete(db, todo)


    # =========================
    # MARK COMPLETE
    # =========================
    def mark_complete(self, db: Session, todo_id: int, owner_id: int):
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if not todo:
            return None

        todo.is_done = True
        db.commit()
        db.refresh(todo)
        return todo


    # =========================
    # LIST + PAGINATION
    # =========================
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
        query = db.query(Todo).filter(
            Todo.owner_id == owner_id,
            Todo.deleted_at.is_(None),  # 🔥 bắt buộc
        )

        if is_done is not None:
            query = query.filter(Todo.is_done == is_done)

        if q:
            query = query.filter(Todo.title.ilike(f"%{q}%"))

        if sort.startswith("-"):
            field = getattr(Todo, sort[1:], Todo.created_at)
            query = query.order_by(desc(field))
        else:
            field = getattr(Todo, sort, Todo.created_at)
            query = query.order_by(asc(field))

        total = query.count()
        items = query.offset(offset).limit(limit).all()

        return items, total


    # =========================
    # OVERDUE
    # =========================
    def get_overdue(self, db: Session, owner_id: int):
        return db.query(Todo).filter(
            Todo.owner_id == owner_id,
            Todo.deleted_at.is_(None),  
            Todo.due_date.isnot(None),
            Todo.due_date < datetime.now(timezone.utc),
        ).all()


    # =========================
    # TODAY
    # =========================
    def get_today(self, db: Session, owner_id: int):
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        return db.query(Todo).filter(
            Todo.owner_id == owner_id,
            Todo.deleted_at.is_(None),  
            Todo.due_date.isnot(None),
            Todo.due_date >= today_start,
            Todo.due_date < today_end,
        ).all()
    
    # =========================
    # LIST TRASH
    # =========================
    def list_deleted(self, db: Session, owner_id: int):
        return self.repository.get_deleted(db, owner_id)


    # =========================
    # RESTORE
    # =========================
    def restore_todo(self, db: Session, todo_id: int, owner_id: int):
        todo = db.query(Todo).filter(
            Todo.id == todo_id,
            Todo.owner_id == owner_id,
            Todo.deleted_at.is_not(None),
        ).first()

        if not todo:
            return None

        return self.repository.restore(db, todo)


    # =========================
    # FORCE DELETE (optional)
    # =========================
    def force_delete(self, db: Session, todo_id: int, owner_id: int):
        todo = db.query(Todo).filter(
            Todo.id == todo_id,
            Todo.owner_id == owner_id,
        ).first()

        if not todo:
            return None

        return self.repository.force_delete(db, todo)