from sqlalchemy.orm import Session
from datetime import datetime
from .model import Todo


class TodoRepository:

    # =========================
    # CREATE
    # =========================
    def create(
        self,
        db: Session,
        owner_id: int,
        title: str,
        description: str | None,
        is_done: bool,
        tags: list,
        due_date=None,
    ):
        todo = Todo(
            title=title,
            description=description,
            is_done=is_done,
            due_date=due_date,
            owner_id=owner_id,
            deleted_at=None,  
        )

        todo.tags = tags

        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo


    # =========================
    # READ
    # =========================
    def get_by_id(self, db: Session, todo_id: int, owner_id: int):
        return (
            db.query(Todo)
            .filter(
                Todo.id == todo_id,
                Todo.owner_id == owner_id,
                Todo.deleted_at.is_(None),   
            )
            .first()
        )


    def get_all(self, db: Session, owner_id: int):
        return (
            db.query(Todo)
            .filter(
                Todo.owner_id == owner_id,
                Todo.deleted_at.is_(None),   
            )
            .all()
        )


    # =========================
    # UPDATE
    # =========================
    def update(
        self,
        db: Session,
        todo: Todo,
        title: str,
        description: str,
        is_done: bool,
        tags: list,
        due_date=None,
    ):
        todo.title = title
        todo.description = description
        todo.is_done = is_done
        todo.tags = tags
        todo.due_date = due_date

        db.commit()
        db.refresh(todo)
        return todo


    # =========================
    # SOFT DELETE
    # =========================
    def soft_delete(self, db: Session, todo: Todo):
        if todo.deleted_at is not None:
            return todo 

        todo.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(todo)
        return todo


  # =========================
    # TRASH LIST
    # =========================
    def get_deleted(self, db: Session, owner_id: int):
        return (
            db.query(Todo)
            .filter(
                Todo.owner_id == owner_id,
                Todo.deleted_at.is_not(None),
            )
            .order_by(Todo.deleted_at.desc())
            .all()
        )


    # =========================
    # RESTORE
    # =========================
    def restore(self, db: Session, todo: Todo):
        todo.deleted_at = None
        db.commit()
        db.refresh(todo)
        return todo


    # =========================
    # FORCE DELETE (optional)
    # =========================
    def force_delete(self, db: Session, todo: Todo):
        db.delete(todo)
        db.commit()
        return True