from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    PaginatedTodoResponse,
    TodoStatusUpdate
)
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from app.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/todos", tags=["Todos"])

repository = TodoRepository()
service = TodoService(repository)



@router.post("/", response_model=TodoResponse, status_code=201)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return service.create_todo(db, todo)


@router.get("/", response_model=PaginatedTodoResponse)
def get_all(
    is_done: bool | None = None,
    q: str | None = None,
    sort: str = Query("created_at", pattern="^-?created_at$"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    items, total = service.list_todos(
        db=db,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{todo_id}", response_model=TodoResponse)
def get_one(todo_id: int, db: Session = Depends(get_db)):
    todo = service.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    todo = service.update_todo(db, todo_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete(todo_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")

@router.patch("/{todo_id}/status", response_model=TodoResponse)
def update_status(
    todo_id: int,
    data: TodoStatusUpdate,
    db: Session = Depends(get_db)
):
    todo = service.update_status(db, todo_id, data.is_done)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/{todo_id}/complete", response_model=TodoResponse)
def mark_complete(todo_id: int, db: Session = Depends(get_db)):
    todo = service.mark_complete(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
