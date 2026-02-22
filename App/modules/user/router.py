from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.user.model import User
from .schema import UserCreate, UserLogin, UserResponse
from .service import UserService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.register(db, user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        return UserService.login(
            db,
            form_data.username,
            form_data.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }