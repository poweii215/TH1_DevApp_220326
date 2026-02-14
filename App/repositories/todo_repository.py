from sqlalchemy.orm import Session
from app.models.todo_model import Todo


class TodoRepository:

    def create(self, db: Session, title: str, description: str | None, is_done: bool):
        todo = Todo(
            title=title,
            description=description,
            is_done=is_done
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Todo).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, todo_id: int):
        return db.query(Todo).filter(Todo.id == todo_id).first()

    def update(self, db: Session, todo: Todo, title: str, description: str, is_done: bool):
        todo.title = title
        todo.description = description
        todo.is_done = is_done
        db.commit()
        db.refresh(todo)
        return todo

    def patch(self, db: Session, todo: Todo, **kwargs):
        for key, value in kwargs.items():
            setattr(todo, key, value)
        db.commit()
        db.refresh(todo)
        return todo

    def delete(self, db: Session, todo: Todo):
        db.delete(todo)
        db.commit()
        return todo
