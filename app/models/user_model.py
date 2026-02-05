from app.core.database import Base
from sqlalchemy import Column, Integer, String, Date


class User(Base):
    __tablename__ = "project2"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    gender = Column(String(20), nullable=False)
    dob = Column(Date, nullable=False) 
    address = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
