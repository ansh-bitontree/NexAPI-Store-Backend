from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserLogin, UserCreate
from app.core.database import get_db
from app.services.user_service import (
                        get_user_by_email, 
                        get_user_by_username,
                        create_user,
                        )
from app.services.auth_service import verify_password, create_access_token
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["Auth"])
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username not available")

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    create_user(db, user)
    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user or not verify_password(user.password,
                                          db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)},
                                ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    }
