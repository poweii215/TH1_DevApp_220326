from fastapi import FastAPI
from app.routers.todo_router import router as todo_router
from app.core.config import settings
from app.core.database import engine
from app.models import todo_model
from app.core.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

@app.get("/health")
def health_check():
    return {"status": "ok"} 
@app.get("/")
def root():
    return {"message": "Welcome to the Todo API!"}
app.include_router(todo_router, prefix="/api/v1")


