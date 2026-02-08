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


class ForgetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_new_password: Optional[str] = None

    @field_validator("dob", mode="before")
    @classmethod
    def validate_optional_dob(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            v = date.fromisoformat(v)

        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, 
                                                                 v.day))

        if v > today:
            raise ValueError("Date of birth cannot be in the future")
        if age < 18:
            raise ValueError("You must be at least 18 years old")
        if age > 110:
            raise ValueError("Age cannot be greater than 110")

        return v


class UserResetPasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str




