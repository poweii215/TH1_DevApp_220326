from sqlalchemy.orm import Session
from .repository import UserRepository
from .model import User
from app.core.security import hash_password, verify_password, create_access_token


class UserService:

    @staticmethod
    def register(db: Session, email: str, password: str):
        existing = UserRepository.get_by_email(db, email)
        if existing:
            raise ValueError("Email already registered")

        user = User(
            email=email,
            hashed_password=hash_password(password)
        )
        return UserRepository.create(db, user)

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}