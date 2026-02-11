from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str                          
    description: Optional[str] = None
    price: float
    discount_percentage: Optional[float] = None  
    quantity: Optional[int] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None            
    rating: Optional[float] = None


class ProductOut(ProductBase):
    id: int
    is_active: bool = True                     
    created_at: Optional[datetime] = None      

    model_config = ConfigDict(from_attributes=True)                 
