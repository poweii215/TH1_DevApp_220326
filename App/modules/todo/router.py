from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.user.model import User
from .schema import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    PaginatedTodoResponse,
)
from .service import TodoService
from .repository import TodoRepository


router = APIRouter(tags=["Todos"])

repository = TodoRepository()
service = TodoService(repository)


# =========================
# CREATE
# =========================
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    data: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create_todo(db, data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# LIST (static route trước)
# =========================
@router.get("/", response_model=PaginatedTodoResponse)
def list_todos(
    is_done: bool | None = Query(default=None),
    q: str | None = Query(default=None),
    sort: str = Query(default="created_at"),
    limit: int = Query(default=10, ge=1),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = service.list_todos(
        db=db,
        owner_id=current_user.id,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )

    return PaginatedTodoResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


# =========================
# STATUS ROUTES (static trước dynamic)
# =========================
@router.get("/status/overdue", response_model=list[TodoResponse])
def overdue_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_overdue(db, current_user.id)


@router.get("/status/today", response_model=list[TodoResponse])
def today_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_today(db, current_user.id)

@router.get("/trash", response_model=list[TodoResponse])
def list_deleted_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_deleted(db, current_user.id)
# =========================
# GET BY ID (dynamic route cuối)
# =========================
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = service.get_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# =========================
# UPDATE
# =========================
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        todo = service.update_todo(db, todo_id, data, current_user.id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# DELETE (Soft Delete)
# =========================
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = service.delete_todo(db, todo_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None


# =========================
# MARK COMPLETE
# =========================
@router.patch("/{todo_id}/complete", response_model=TodoResponse)
def mark_complete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = service.mark_complete(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo



@router.patch("/{todo_id}/restore", response_model=TodoResponse)
def restore_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = service.restore_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Deleted todo not found")
    return todo

@router.delete("/{todo_id}/force", status_code=204)
def force_delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = service.force_delete(db, todo_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None