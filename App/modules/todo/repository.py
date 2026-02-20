from sqlalchemy.orm import Session
from .model import Todo


class TodoRepository:

    def create(self, db: Session, owner_id: int, title: str, description: str | None, is_done: bool):
        todo = Todo(
            title=title,
            description=description,
            is_done=is_done,
            owner_id=owner_id,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def get_by_id(self, db: Session, todo_id: int, owner_id: int):
        return (
            db.query(Todo)
            .filter(Todo.id == todo_id, Todo.owner_id == owner_id)
            .first()
        )

    def delete(self, db: Session, todo: Todo):
        db.delete(todo)
        db.commit()
        return True
    
   
    def update(self, db: Session, todo: Todo, title: str, description: str, is_done: bool):
        todo.title = title
        todo.description = description
        todo.is_done = is_done

        db.commit()
        db.refresh(todo)
        return todo