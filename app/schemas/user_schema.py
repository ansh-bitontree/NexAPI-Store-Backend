from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date


class DOBMixin(BaseModel):
    dob: date

    @field_validator("dob", mode="before")
    @classmethod
    def validate_dob(cls, val):
        if isinstance(val, str):
            val = date.fromisoformat(val)

        today = date.today()
        age = today.year - val.year - ((today.month, today.day) < (val.month, 
                                                                   val.day))

        if val > today:
            raise ValueError("Date of birth cannot be in the future")
        if age < 18:
            raise ValueError("You must be at least 18 years old")
        if age > 110:
            raise ValueError("Age cannot be greater than 110")

        return val

    
class UserBase(BaseModel):
    username: str
    email: EmailStr
    address: Optional[str] = None
    gender: Optional[str] = None


class UserCreate(DOBMixin, UserBase):
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str





