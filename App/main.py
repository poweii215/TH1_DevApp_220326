from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine

# Import models để SQLAlchemy tạo bảng
from app.modules.todo.model import Todo
from app.modules.user.model import User

# Import routers
from app.modules.todo.router import router as todo_router
from app.modules.user.router import router as user_router

# Tạo database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "debug_mode": settings.DEBUG
    }

# Include routers
app.include_router(todo_router, prefix="/todos")    
app.include_router(user_router, prefix="/auth")    