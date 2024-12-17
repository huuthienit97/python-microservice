from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: str = None
    
    class Config:
        from_attributes = True

    @classmethod
    def from_db(cls, db_user: dict):
        db_user["id"] = db_user.pop("_key", None)
        return cls(**db_user)
