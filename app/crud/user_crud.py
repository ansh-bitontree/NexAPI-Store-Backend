from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import hash_password
from app.schemas.user_schema import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email.lower(),
        address=user.address,
        dob=user.dob,
        gender=user.gender,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
