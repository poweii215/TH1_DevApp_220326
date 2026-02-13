from fastapi import FastAPI
from app.routers.todo_router import router as todo_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.include_router(todo_router, prefix="/api/v1")
