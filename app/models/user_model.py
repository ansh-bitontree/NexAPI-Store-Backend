from app.core.database import Base
from sqlalchemy import Column, Integer, String, Date


class User(Base):
    __tablename__ = "nextapi-users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    gender = Column(String(20), nullable=False)
    dob = Column(Date, nullable=False) 
    address = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)