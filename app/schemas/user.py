from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    new_password: Optional[str] = None
    new_password_confirm: Optional[str] = None
    current_password: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserRead(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None
    username: str 
    email: EmailStr
    bio: Optional[str] = None
    avatar: Optional[str] = None
    createdAt: datetime

    class Config:
        orm_mode = True
        fields = {
            'createdAt': 'created_at'
        }


class Token(BaseModel):
    access_token: str
    token_type: str
    
    model_config = {
        "from_attributes": True
    }