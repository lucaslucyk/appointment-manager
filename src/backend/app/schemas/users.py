from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr


class UserBase(BaseModel):
    email: EmailStr
    # role: int

class UserCreate(UserBase):
    password: SecretStr
    is_active: Optional[bool]


class UserUpdate(UserCreate):
    email: Optional[SecretStr]
    password: Optional[SecretStr]
    is_active: Optional[bool]

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
