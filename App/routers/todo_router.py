from fastapi import APIRouter, HTTPException, Query
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    PaginatedTodoResponse
)
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService


router = APIRouter(prefix="/todos", tags=["Todos"])

repository = TodoRepository()
service = TodoService(repository)


@router.post("/", response_model=TodoResponse, status_code=201)
def create(todo: TodoCreate):
    return service.create_todo(todo)


@router.get("/", response_model=PaginatedTodoResponse)
def get_all(
    is_done: bool | None = None,
    q: str | None = None,
    sort: str = Query("created_at", pattern="^-?created_at$"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    items, total = service.list_todos(is_done, q, sort, limit, offset)
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{todo_id}", response_model=TodoResponse)
def get_one(todo_id: int):
    todo = service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update(todo_id: int, data: TodoUpdate):
    todo = service.update_todo(todo_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete(todo_id: int):
    deleted = service.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
