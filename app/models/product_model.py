from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  
    description = Column(Text)
    price = Column(Integer, nullable=False)
    discount_percentage = Column(Float, default=0.0)          
    quantity = Column(Integer, default=0)
    category = Column(String(100), index=True)
    brand = Column(String(100))
    image_url = Column(String(500))              
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, nullable=True)                
    is_active = Column(Boolean, default=True)   
